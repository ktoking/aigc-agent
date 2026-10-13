"""Fast, dated public-news discovery; no model or platform browser calls."""
import asyncio
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

import feedparser
import httpx
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from .models import AgentRun, Topic, now
from .service import WorkflowError, serialize

RUN_NAME = "Hotspot Refresh"
CACHE_SECONDS = 15 * 60
TOTAL_TIMEOUT = 12
MAX_ITEMS = 20
_tasks = {}
BAIDU_URL = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
CHINA_URL = "https://www.chinanews.com.cn/rss/scroll-news.xml"
BBC_URL = "https://feeds.bbci.co.uk/zhongwen/simp/rss.xml"


def _direction(value):
    value = " ".join(value.split())
    if len(value) > 300:
        raise WorkflowError("热点方向请控制在 300 字以内")
    return value


def _key(direction):
    date = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
    return date + ":" + hashlib.sha256(direction.casefold().encode()).hexdigest()[:20]


def task_view(run, cache_hit=False):
    value = run.result or {}
    return {"id": run.id, "status": run.status, "stage": value.get("stage", "FETCHING"),
            "direction": value.get("direction", ""), "cache_hit": cache_hit,
            "topic_ids": value.get("topic_ids", []), "count": len(value.get("topic_ids", [])),
            "sources": value.get("sources", []), "errors": value.get("errors", []),
            "error": value.get("error"), "created_at": run.created_at,
            "finished_at": run.finished_at, "result": value}


def get_task(session, task_id):
    run = session.get(AgentRun, task_id)
    if not run or run.name != RUN_NAME:
        raise WorkflowError("未找到热点刷新任务")
    return task_view(run)


def _runs(session, key):
    return [run for run in session.scalars(select(AgentRun).where(AgentRun.name == RUN_NAME)
            .order_by(AgentRun.created_at.desc())).all() if (run.result or {}).get("cache_key") == key]


def _fresh(run):
    if run.status != "COMPLETED" or not run.finished_at:
        return False
    return (datetime.now(timezone.utc) - datetime.fromisoformat(run.finished_at)).total_seconds() < CACHE_SECONDS


def list_hotspots(session, direction=""):
    direction = _direction(direction)
    runs = _runs(session, _key(direction))
    latest = runs[0] if runs else None
    completed = next((run for run in runs if run.status == "COMPLETED"), None)
    ids = (completed.result or {}).get("topic_ids", []) if completed else []
    topics = {topic.id: topic for topic in session.scalars(select(Topic).where(Topic.id.in_(ids))).all()} if ids else {}
    value = latest.result or {} if latest else {}
    return {"items": [serialize(topics[topic_id]) for topic_id in ids if topic_id in topics],
            "updated_at": completed.finished_at if completed else None,
            "loading": bool(latest and latest.status == "RUNNING"),
            "sources": value.get("sources", []), "errors": value.get("errors", []),
            "task_id": latest.id if latest else None, "status": latest.status if latest else "EMPTY",
            "direction": direction, "cache_fresh": bool(completed and _fresh(completed))}


def recover_tasks(session):
    """Call at startup only: preserve durable records, never auto-restart network work."""
    for run in session.scalars(select(AgentRun).where(AgentRun.name == RUN_NAME, AgentRun.status == "RUNNING")):
        if run.id not in _tasks:
            run.status = "INTERRUPTED"
            run.finished_at = now()
            run.result = {**(run.result or {}), "stage": "INTERRUPTED", "errors": ["服务重启中断刷新，可重新获取热点"]}
    session.commit()


async def start_refresh(session, direction="", session_factory=None):
    direction = _direction(direction)
    key = _key(direction)
    runs = _runs(session, key)
    for run in runs:
        if run.status == "RUNNING" and run.id in _tasks:
            return task_view(run)
        if _fresh(run):
            return task_view(run, cache_hit=True)
    # A stale running record cannot make the UI spin forever after a process restart.
    recover_tasks(session)
    run = AgentRun(name=RUN_NAME, mode="live", result={"direction": direction, "cache_key": key,
                   "stage": "FETCHING", "topic_ids": [], "sources": [], "errors": []})
    session.add(run)
    session.commit()
    view = task_view(run)
    factory = session_factory or sessionmaker(bind=session.get_bind(), expire_on_commit=False)
    task = asyncio.create_task(execute_refresh(run.id, factory))
    _tasks[run.id] = task
    task.add_done_callback(lambda _: _tasks.pop(run.id, None))
    return view


def _safe_url(value):
    try:
        parsed = urlsplit(value or "")
        if parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username and not parsed.password:
            return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
    except ValueError:
        pass
    return ""


def _matches(title, direction):
    return not direction or direction.casefold() in title.casefold()


def _entry(title, url, source, retrieved_at, **evidence):
    return {"title": title.strip(), "url": url, "source": source, "retrieved_at": retrieved_at,
            **evidence}


def _baidu(data, direction, retrieved_at):
    if not data.get("success"):
        raise ValueError("热榜接口未返回成功状态")
    entries = []
    # This nested schema was verified against the public endpoint, not guessed.
    for card in data.get("data", {}).get("cards", []):
        for group in card.get("content", []):
            for item in group.get("content", []):
                title, url = item.get("word", ""), _safe_url(item.get("url"))
                if title and url and not item.get("isTop") and _matches(title, direction):
                    entries.append(_entry(title, url, "百度实时热榜", retrieved_at,
                                          rank=item.get("index"), kind="ranking", published_at=None,
                                          time_basis="获取时的公开热榜；未提供新闻发布时间"))
    return entries[:MAX_ITEMS]


def _rss(text, source, direction, retrieved_at, *, search=False):
    feed = feedparser.parse(text)
    if not feed.entries and feed.bozo:
        raise ValueError("资讯源不是有效 RSS")
    current = datetime.fromisoformat(retrieved_at)
    entries = []
    for item in feed.entries:
        parsed_date = item.get("published_parsed") or item.get("updated_parsed")
        if not parsed_date:
            continue  # undated/old material cannot masquerade as recent news
        published = datetime(*parsed_date[:6], tzinfo=timezone.utc)
        age = current - published
        if age > timedelta(hours=72) or age < timedelta(minutes=-10):
            continue
        title, url = item.get("title", ""), _safe_url(item.get("link"))
        if not title or not url or (not search and not _matches(title, direction)):
            continue
        entries.append(_entry(title, url, source, retrieved_at, kind="news", rank=None,
                       published_at=published.isoformat(), age_hours=round(age.total_seconds() / 3600, 1),
                       time_basis="最近24小时" if age <= timedelta(hours=24) else "最近72小时"))
        if len(entries) >= MAX_ITEMS:
            break
    return entries


async def collect_sources(direction=""):
    """Every source is read concurrently with per-source and overall hard deadlines."""
    retrieved_at = now()
    parameters = {"hl": "zh-CN", "gl": "CN", "ceid": "CN:zh-Hans"}
    google_path = "https://news.google.com/rss"
    if direction:
        google_path += "/search"
        parameters["q"] = direction + " when:1d"
    providers = [("百度实时热榜", BAIDU_URL, "baidu"),
                 ("Google News", google_path + "?" + urlencode(parameters), "search" if direction else "rss"),
                 ("中国新闻网", CHINA_URL, "rss")]
    if not direction:
        providers.append(("BBC中文", BBC_URL, "rss"))
    async with httpx.AsyncClient(timeout=httpx.Timeout(5, connect=3), trust_env=False,
                                 follow_redirects=True, headers={"User-Agent": "XHS-Growth-Agent/1.0 (public news reader)"}) as client:
        async def fetch(name, url, kind):
            try:
                async with asyncio.timeout(5):
                    response = await client.get(url)
                    response.raise_for_status()
                    if len(response.content) > 3_000_000:
                        raise ValueError("资讯源响应过大")
                    items = _baidu(response.json(), direction, retrieved_at) if kind == "baidu" else _rss(
                        response.text, name, direction, retrieved_at, search=kind == "search")
                    return {"name": name, "url": url, "items": items,
                            "error": None if items else name + "：没有匹配方向的近期条目"}
            except Exception as error:
                # Do not persist raw upstream text, query credentials, or traces.
                return {"name": name, "url": url, "items": [], "error": name + "：读取失败（" + type(error).__name__ + "）"}
        pending = [asyncio.create_task(fetch(*provider)) for provider in providers]
        done, unfinished = await asyncio.wait(pending, timeout=TOTAL_TIMEOUT)
        for task in unfinished:
            task.cancel()
        if unfinished:
            await asyncio.gather(*unfinished, return_exceptions=True)
        output = []
        for provider, task in zip(providers, pending):
            output.append(task.result() if task in done else {"name": provider[0], "url": provider[1], "items": [],
                                                               "error": provider[0] + "：达到总耗时上限"})
        return output


def _merge(results):
    # Round robin keeps default results visibly multi-source instead of 20 entries from the first feed.
    entries, by_title, by_url = [], {}, {}
    for index in range(MAX_ITEMS):
        for result in results:
            if index >= len(result["items"]):
                continue
            entry = result["items"][index]
            title = re.sub(r"\s+-\s+[^-]+$", "", entry["title"])
            title_key = re.sub(r"\W+", "", title.casefold())
            existing = by_title.get(title_key)
            if existing is None:
                existing = by_url.get(entry["url"])
            if existing is not None:
                by_title[title_key] = by_url[entry["url"]] = existing
                if entry not in entries[existing]["entries"]:
                    entries[existing]["entries"].append(entry)
                continue
            if len(entries) >= MAX_ITEMS:
                continue
            by_title[title_key] = by_url[entry["url"]] = len(entries)
            entries.append({"title": entry["title"], "entries": [entry]})
    return entries


async def execute_refresh(task_id, factory):
    try:
        with factory() as session:
            payload = dict(session.get(AgentRun, task_id).result)
        async with asyncio.timeout(TOTAL_TIMEOUT):
            results = await collect_sources(payload["direction"])
        merged = _merge(results)
        errors = [result["error"] for result in results if result["error"]]
        sources = [result["name"] for result in results if result["items"]]
        ids = []
        with factory() as session:
            for entry in merged:
                proof = entry["entries"]
                fingerprint = hashlib.sha256(json.dumps([payload["cache_key"], entry["title"]], ensure_ascii=False).encode()).hexdigest()
                topic = session.scalar(select(Topic).where(Topic.fingerprint == fingerprint))
                source_list = [{"title": item["title"], "url": item["url"], "source": item["source"],
                    "verified": True, "retrieved_at": item["retrieved_at"], "published_at": item["published_at"],
                    "verification_scope": "已读取公开热榜或RSS条目；尚未逐项核实新闻事实"} for item in proof]
                evidence = {"source": "hotspot", "direction": payload["direction"], "cache_key": payload["cache_key"],
                    "retrieved_at": proof[0]["retrieved_at"], "published_at": proof[0]["published_at"],
                    "rank": proof[0]["rank"], "time_basis": proof[0]["time_basis"], "entries": proof,
                    "method": "多来源公开资讯；来源读取不等于新闻事实核验"}
                if not topic:
                    topic = Topic(title=entry["title"], category=payload["direction"] or "热点资讯", score=0,
                        reasons=[proof[0]["time_basis"], "选择后按你的方向创作"], sources=source_list,
                        mode="live", fingerprint=fingerprint, evidence=evidence)
                    session.add(topic)
                    session.flush()
                else:
                    topic.sources, topic.evidence = source_list, evidence
                ids.append(topic.id)
            run = session.get(AgentRun, task_id)
            run.status = "COMPLETED" if ids else "BLOCKED"
            run.finished_at = now()
            run.result = {**payload, "stage": "DONE" if ids else "BLOCKED", "topic_ids": ids,
                          "sources": sources, "errors": errors,
                          "error": None if ids else "没有获取到相关近期热点，请更换方向或稍后刷新"}
            session.commit()
    except asyncio.CancelledError:
        _finish_error(factory, task_id, "INTERRUPTED", "热点刷新中断，可重新获取")
        raise
    except Exception as error:
        detail = "达到12秒刷新上限" if isinstance(error, TimeoutError) else "热点读取失败（" + type(error).__name__ + "）"
        _finish_error(factory, task_id, "BLOCKED", detail)


def _finish_error(factory, task_id, status, detail):
    with factory() as session:
        run = session.get(AgentRun, task_id)
        run.status, run.finished_at = status, now()
        run.result = {**(run.result or {}), "stage": status, "errors": [detail], "error": detail}
        session.commit()
