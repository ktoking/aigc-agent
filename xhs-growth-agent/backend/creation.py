"""Short HTTP requests, durable progress and direct direction-to-review creation."""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from .db import SessionLocal
from .model_client import ModelClient, ModelUnavailable
from .models import AgentRun, Topic, now
from .service import WorkflowError, make_article, settings

RUN_NAME = "Content Creation"
_tasks = set()


def _recent(value):
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        current = datetime.fromisoformat(now())
        return stamp.tzinfo is not None and current - timedelta(hours=72) <= stamp <= current + timedelta(minutes=5)
    except (AttributeError, TypeError, ValueError):
        return False


def task_view(run):
    result = run.result or {}
    return {"id": run.id, "status": run.status, "stage": result.get("stage", "QUEUED"),
            "direction": result.get("direction", ""), "count": result.get("count", 1),
            "completed": len(result.get("article_ids", [])), "article_ids": result.get("article_ids", []),
            "error": result.get("error"), "created_at": run.created_at,
            "updated_at": result.get("updated_at", run.created_at), "finished_at": run.finished_at}


def get_task(session, task_id):
    run = session.get(AgentRun, task_id)
    if not run or run.name != RUN_NAME:
        raise WorkflowError("未找到创作任务")
    return task_view(run)


def latest_task(session):
    run = session.scalar(select(AgentRun).where(AgentRun.name == RUN_NAME).order_by(AgentRun.created_at.desc()).limit(1))
    return task_view(run) if run else None


async def start_task(session, direction, count=1, topic_ids=None, material="", session_factory=None):
    direction, material = direction.strip(), material.strip()
    if not direction or len(direction) > 300:
        raise WorkflowError("请填写 1 至 300 字的内容方向")
    if type(count) is not int or not 1 <= count <= 3:
        raise WorkflowError("每次生成 1 至 3 篇")
    if len(material) > 10000:
        raise WorkflowError("参考素材请控制在 10000 字以内")
    topic_ids = list(dict.fromkeys(topic_ids or []))
    if len(topic_ids) > 5:
        raise WorkflowError("每次最多选择 5 个热点")
    if session.scalar(select(AgentRun.id).where(AgentRun.name == RUN_NAME, AgentRun.status == "RUNNING").limit(1)):
        raise WorkflowError("已有创作任务进行中，可在审核中心查看进度")
    selected = []
    for topic_id in topic_ids:
        topic = session.get(Topic, topic_id)
        if (not topic or topic.mode != "live" or topic.evidence.get("source") != "hotspot"
                or not _recent(topic.created_at)
                or not any(source.get("verified") and _recent(source.get("retrieved_at")) for source in topic.sources)):
            raise WorkflowError("请选择最近 72 小时读取的真实热点，历史研究或测试样本不能作为今日热点")
        selected.append({"topic_id": topic.id, "title": topic.title, "sources": topic.sources, "evidence": topic.evidence})
    result = {"stage": "QUEUED", "direction": direction, "count": count, "article_ids": [],
              "material": material, "selected_topics": selected, "error": None, "updated_at": now()}
    run = AgentRun(name=RUN_NAME, mode="live", result=result)
    session.add(run)
    session.commit()
    view = task_view(run)
    factory = session_factory or sessionmaker(bind=session.get_bind(), expire_on_commit=False)
    work = asyncio.create_task(execute_task(run.id, factory))
    _tasks.add(work)
    work.add_done_callback(_tasks.discard)
    return view


def _progress(factory, task_id, stage, *, article_id=None, error=None, status=None):
    with factory() as session:
        run = session.get(AgentRun, task_id)
        value = dict(run.result)
        value["stage"] = stage
        value["updated_at"] = now()
        if article_id:
            value["article_ids"] = [*value["article_ids"], article_id]
        if error:
            value["error"] = error
        run.result = value
        if status:
            run.status = status
            run.finished_at = now()
        session.commit()


def _make(factory, data):
    # The synchronous browser renderer and its session stay on one worker thread.
    with factory() as session:
        return make_article(session, data, mode="live").id


async def execute_task(task_id, factory=SessionLocal):
    try:
        with factory() as session:
            payload = dict(session.get(AgentRun, task_id).result)
        sources = []
        for topic in payload["selected_topics"]:
            for source in topic["sources"]:
                if source not in sources:
                    sources.append(source)
        verified = any(source.get("verified") for source in sources)
        for index in range(payload["count"]):
            _progress(factory, task_id, "WRITING")
            brief = {"direction": payload["direction"], "material": payload["material"],
                     "selected_topics": payload["selected_topics"], "sources": sources,
                     "content_kind": "source_based" if verified else "general_advice",
                     "article_number": index + 1, "article_count": payload["count"],
                     "previous_titles": payload.get("titles", []),
                     "requirements": "只围绕用户指定方向，不沿用账号旧AI定位。2至3张精简内容卡片，每篇切入点不同。"
                                     "没有已核验新闻或具体价格材料时，不编造最新事件、地址、价格、营业时间、热门程度。"
                                     "可写通用建议或准备清单，不假装作者亲测、到店、旅行、买过或获得成效。"
                                     "用户素材只作为用户输入，不能称为已独立核验。"}
            with factory() as session:
                config = settings(session)
                config["account_positioning"] = payload["direction"]
                data = await ModelClient().write(session, brief, config)
            data.update(sources=sources, category=payload["direction"][:80], style="素材分享" if verified else "通用建议")
            _progress(factory, task_id, "RENDERING")
            article_id = await asyncio.to_thread(_make, factory, data)
            payload.setdefault("titles", []).append(data["title"])
            _progress(factory, task_id, "REVIEW_READY", article_id=article_id)
        _progress(factory, task_id, "DONE", status="COMPLETED")
    except asyncio.CancelledError:
        _progress(factory, task_id, "INTERRUPTED", error="任务中断，已生成的草稿仍可审核", status="INTERRUPTED")
        raise
    except Exception as error:
        detail = str(error) if isinstance(error, (ModelUnavailable, WorkflowError)) else "创作未完成，请查看任务记录后重试"
        _progress(factory, task_id, "FAILED", error=detail, status="FAILED")
