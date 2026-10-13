import asyncio
import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
from backend import creation
from backend.models import AgentRun, Article, ContentBrief, PublishJob, Topic, now
from backend.model_client import ModelUnavailable
from backend.service import WorkflowError, recover


def factory(session):
    return sessionmaker(bind=session.get_bind(), expire_on_commit=False)


def output(title="周末散步准备清单"):
    return {"title": title, "title_candidates": [title, "散步前做点准备", "轻松散步的小建议"],
            "body": "安排周末散步时，可以先选一个容易抵达的区域，留出回程时间。穿舒适的鞋，带水，关注当天的天气。" * 4,
            "tags": ["周末散步"], "cards": [{"title": f"第{i}步", "body": f"散步建议{i}"} for i in range(3)],
            "comment_prompt": "你想走哪一段？"}


async def drained():
    await asyncio.gather(*list(creation._tasks))


@pytest.mark.asyncio
async def test_fast_response_direction_to_review_no_old_briefs(session, render_stub, monkeypatch):
    started, release = asyncio.Event(), asyncio.Event()
    captured = []
    async def write(_client, _session, brief, config):
        captured.append((brief, config))
        started.set()
        await release.wait()
        return output()
    monkeypatch.setattr(creation.ModelClient, "write", write)
    session.add(ContentBrief(topic_id="old_ai_topic", data={"title": "旧AI策划", "sources": []}))
    session.commit()
    task = await creation.start_task(session, "周末城市散步", material="想写准备清单，不假装亲测", session_factory=factory(session))
    assert task["status"] == "RUNNING" and task["stage"] == "QUEUED"
    await started.wait()
    assert creation.get_task(session, task["id"])["article_ids"] == []
    with pytest.raises(WorkflowError, match="已有创作任务"):
        await creation.start_task(session, "美食", session_factory=factory(session))
    release.set()
    await drained()
    session.expire_all()
    task = creation.get_task(session, task["id"])
    article = session.get(Article, task["article_ids"][0])
    assert task["status"] == "COMPLETED" and task["completed"] == 1
    assert article.category == "周末城市散步" and article.style == "通用建议" and article.sources == []
    assert article.status == "PENDING_REVIEW"
    assert session.scalar(select(func.count(PublishJob.id))) == 0
    assert session.scalar(select(ContentBrief)).status == "PLANNED"
    assert captured[0][0]["direction"] == "周末城市散步"
    assert captured[0][1]["account_positioning"] == "周末城市散步"


@pytest.mark.asyncio
async def test_source_only_explicit_selection(session, render_stub, monkeypatch):
    source = {"title": "天气服务", "url": "https://example.com/weather", "verified": True, "retrieved_at": now()}
    topic = Topic(title="城市天气", sources=[source], fingerprint="selected", mode="live", evidence={"source": "hotspot"})
    unrelated = Topic(title="AI新模型", sources=[{"url": "https://example.com/ai", "verified": True}], fingerprint="old", mode="live")
    session.add_all([topic, unrelated])
    session.commit()
    seen = []
    async def write(_client, _session, brief, _settings):
        seen.append(brief)
        return output()
    monkeypatch.setattr(creation.ModelClient, "write", write)
    task = await creation.start_task(session, "城市散步", topic_ids=[topic.id], session_factory=factory(session))
    await drained()
    session.expire_all()
    article = session.get(Article, creation.get_task(session, task["id"])["article_ids"][0])
    assert article.sources == [source] and article.status == "PENDING_REVIEW"
    assert seen[0]["content_kind"] == "source_based" and len(seen[0]["selected_topics"]) == 1


@pytest.mark.asyncio
async def test_partial_task_keeps_completed_draft_after_model_failure(session, render_stub, monkeypatch):
    count = 0
    async def write(_client, _session, brief, _settings):
        nonlocal count
        count += 1
        if count == 2:
            assert brief["previous_titles"] == ["周末散步准备清单"]
            raise ModelUnavailable("调用超时，没有平台提交")
        return output()
    monkeypatch.setattr(creation.ModelClient, "write", write)
    task = await creation.start_task(session, "城市散步", count=2, session_factory=factory(session))
    await drained()
    session.expire_all()
    result = creation.get_task(session, task["id"])
    assert result["status"] == "FAILED" and result["completed"] == 1
    assert "超时" in result["error"] and session.scalar(select(func.count(PublishJob.id))) == 0


@pytest.mark.asyncio
async def test_validation_no_task_or_platform_effect(session):
    for params in ({"direction": " "}, {"direction": "x" * 301}, {"direction": "散步", "count": 4},
                   {"direction": "散步", "count": True}, {"direction": "散步", "topic_ids": ["missing"]},
                   {"direction": "散步", "material": "x" * 10001}):
        with pytest.raises(WorkflowError):
            await creation.start_task(session, **params, session_factory=factory(session))
    assert session.scalar(select(func.count(AgentRun.id))) == 0
    with pytest.raises(WorkflowError):
        creation.get_task(session, "missing")
    assert creation.latest_task(session) is None


def test_restart_interrupts_creation_without_retry(session):
    task = AgentRun(name=creation.RUN_NAME, mode="live", result={"stage": "WRITING", "direction": "散步", "article_ids": []})
    session.add(task)
    session.commit()
    recover(session)
    assert creation.get_task(session, task.id)["status"] == "INTERRUPTED"
    assert session.scalar(select(func.count(PublishJob.id))) == 0


@pytest.mark.asyncio
async def test_old_live_candidates_and_stale_hotspots_are_rejected(session):
    topics = [
        Topic(title="旧研究", sources=[{"verified": True, "retrieved_at": now()}], fingerprint="old-research", mode="live", evidence={"source": "rss"}),
        Topic(title="过期热点", sources=[{"verified": True, "retrieved_at": "2026-01-01T00:00:00+08:00"}], fingerprint="stale", mode="live", evidence={"source": "hotspot"}),
    ]
    session.add_all(topics)
    session.commit()
    for topic in topics:
        with pytest.raises(WorkflowError, match="72"):
            await creation.start_task(session, "散步", topic_ids=[topic.id], session_factory=factory(session))
    assert session.scalar(select(func.count(AgentRun.id))) == 0
