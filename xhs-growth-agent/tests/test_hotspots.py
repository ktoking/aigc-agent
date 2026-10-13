import asyncio
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
import time

import pytest
from sqlalchemy import select

from backend import hotspots
from backend.models import AgentRun, Topic, now


def result(title="周末旅游清单", source="新闻源", url="https://example.com/travel"):
    entry = hotspots._entry(title, url, source, now(), kind="news", rank=None,
                           published_at=now(), time_basis="最近24小时")
    return {"name": source, "url": "https://example.com/feed", "items": [entry], "error": None}


async def wait_task(task_id):
    task = hotspots._tasks.get(task_id)
    if task:
        await task
    await asyncio.sleep(0)


async def test_refresh_returns_promptly_then_persists_and_cache_avoids_network(session, monkeypatch):
    calls = []
    release = asyncio.Event()
    async def collect(direction):
        calls.append(direction)
        await release.wait()
        return [result()]
    monkeypatch.setattr(hotspots, "collect_sources", collect)
    begin = time.monotonic()
    first = await hotspots.start_refresh(session, "  旅游  ")
    assert time.monotonic() - begin < 0.2
    assert first["status"] == "RUNNING"
    assert hotspots.list_hotspots(session, "旅游")["loading"]
    duplicate = await hotspots.start_refresh(session, "旅游")
    assert duplicate["id"] == first["id"]
    release.set()
    await wait_task(first["id"])
    session.expire_all()
    finished = hotspots.get_task(session, first["id"])
    assert finished["status"] == "COMPLETED"
    assert finished["count"] == 1
    listed = hotspots.list_hotspots(session, "旅游")
    assert not listed["loading"] and listed["cache_fresh"]
    assert listed["items"][0]["category"] == "旅游"
    assert listed["items"][0]["mode"] == "live"
    cached = await hotspots.start_refresh(session, "旅游")
    assert cached["cache_hit"]
    assert calls == ["旅游"]
    assert hotspots.list_hotspots(session, "美食")["items"] == []


async def test_all_failed_marks_blocked_no_fabricated_topics(session, monkeypatch):
    async def collect(_):
        return [{"name": "资讯源", "items": [], "url": "https://example.com", "error": "读取失败"}]
    monkeypatch.setattr(hotspots, "collect_sources", collect)
    task = await hotspots.start_refresh(session)
    await wait_task(task["id"])
    session.expire_all()
    state = hotspots.get_task(session, task["id"])
    assert state["status"] == "BLOCKED" and state["errors"] == ["读取失败"]
    assert session.scalars(select(Topic)).all() == []


async def test_total_deadline_marks_blocked(session, monkeypatch):
    async def collect(_):
        await asyncio.sleep(30)
    monkeypatch.setattr(hotspots, "collect_sources", collect)
    monkeypatch.setattr(hotspots, "TOTAL_TIMEOUT", 0.03)
    task = await hotspots.start_refresh(session)
    await wait_task(task["id"])
    session.expire_all()
    assert hotspots.get_task(session, task["id"])["status"] == "BLOCKED"


def test_recovery_preserves_durable_record(session):
    run = AgentRun(name=hotspots.RUN_NAME, mode="live", result={"cache_key": hotspots._key("旅行")})
    session.add(run)
    session.commit()
    hotspots.recover_tasks(session)
    assert run.status == "INTERRUPTED" and run.finished_at
    assert hotspots.get_task(session, run.id)["errors"]


def test_rss_rejects_old_undated_future_and_accepts_72h_with_clear_age():
    current = datetime.now(timezone.utc)
    entries = []
    for name, hours in [("今日", 2), ("前日", 36), ("旧资料", 100), ("未来", -3)]:
        entries.append(f'<item><title>{name}旅游</title><link>https://example.com/{name}</link>'
                       f'<pubDate>{format_datetime(current - timedelta(hours=hours))}</pubDate></item>')
    entries.append('<item><title>没有日期旅游</title><link>https://example.com/no-date</link></item>')
    feed = '<rss version="2.0"><channel>' + ''.join(entries) + '</channel></rss>'
    parsed = hotspots._rss(feed, "新闻", "旅游", current.isoformat())
    assert [row["title"] for row in parsed] == ["今日旅游", "前日旅游"]
    assert [row["time_basis"] for row in parsed] == ["最近24小时", "最近72小时"]
    assert hotspots._rss(feed, "新闻", "美食", current.isoformat()) == []


def test_baidu_actual_schema_keeps_rank_and_no_invented_news_time():
    payload = {"success": True, "data": {"cards": [{"content": [{"content": [
        {"word": "置顶", "url": "https://example.com/top", "isTop": True},
        {"word": "旅游新动态", "url": "https://example.com/travel", "index": 3},
        {"word": "美食新动态", "url": "javascript:alert(1)", "index": 4}]}]}]}}
    parsed = hotspots._baidu(payload, "旅游", now())
    assert len(parsed) == 1 and parsed[0]["rank"] == 3
    assert parsed[0]["published_at"] is None
    assert "获取时" in parsed[0]["time_basis"]


def test_merge_deduplicates_first_item_by_title_and_url_and_caps_results():
    rows = [result(), result(source="另一个源"), result(title="另一标题", url="https://example.com/travel")]
    rows.append({"name": "更多源", "items": [result(title=f"新闻{i}", url=f"https://example.com/{i}")["items"][0]
                                            for i in range(40)], "error": None})
    merged = hotspots._merge(rows)
    assert len(merged) == 20
    assert len(merged[0]["entries"]) == 3
    assert len({item["title"] for item in merged}) == 20


def test_invalid_or_other_run_not_exposed_as_hotspot(session):
    run = AgentRun(name="Content Creation", result={})
    session.add(run)
    session.commit()
    with pytest.raises(ValueError, match="未找到"):
        hotspots.get_task(session, run.id)
    with pytest.raises(ValueError, match="300"):
        hotspots.list_hotspots(session, "旅" * 301)


async def test_expired_cache_refresh_updates_same_topic_without_duplicates(session, monkeypatch):
    async def collect(_):
        return [result()]
    monkeypatch.setattr(hotspots, "collect_sources", collect)
    first = await hotspots.start_refresh(session, "旅游")
    await wait_task(first["id"])
    session.expire_all()
    run = session.get(AgentRun, first["id"])
    run.finished_at = (datetime.now(timezone.utc) - timedelta(minutes=20)).isoformat()
    session.commit()
    assert not hotspots.list_hotspots(session, "旅游")["cache_fresh"]
    second = await hotspots.start_refresh(session, "旅游")
    assert second["id"] != first["id"]
    await wait_task(second["id"])
    session.expire_all()
    assert len(session.scalars(select(Topic)).all()) == 1
    assert hotspots.get_task(session, second["id"])["topic_ids"] == hotspots.get_task(session, first["id"])["topic_ids"]


def test_dedup_google_publisher_suffix_and_aliases():
    first = result(title="周末旅游清单 - 新华社", url="https://example.com/a")
    second = result(title="周末旅游清单", url="https://example.com/b")
    third = result(title="周末旅行准备", url="https://example.com/a")
    fourth = result(title="周末旅行准备", url="https://example.com/c")
    assert len(hotspots._merge([first, second, third, fourth])) == 1
