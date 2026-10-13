import asyncio
from contextlib import contextmanager
import time
import httpx
import pytest
from fastapi import BackgroundTasks
from backend.control import pause_requested
from backend.service import PublishingAgent, settings
from tests.test_api import client
from tests.test_workflow import FakeAdapter, ready

@pytest.mark.asyncio
async def test_status_poll_never_launches_mcp_while_publishing_or_uncertain(monkeypatch):
    import backend.main as api
    def forbidden_adapter(*args):
        raise AssertionError("polling must not launch competing MCP browsers")
    monkeypatch.setattr(api, "XiaohongshuMcpAdapter", forbidden_adapter)
    monkeypatch.setattr(api, "_health_cache", {"at": 0, "url": "http://local/mcp", "value": {"connected": True, "logged_in": True, "detail": "previous status", "tools": []}})
    async with PublishingAgent._lock:
        result = await asyncio.wait_for(api.mcp_health("http://local/mcp"), 0.1)
    assert result["stale"] and result["connected"]
    result = await asyncio.wait_for(api.mcp_health("http://local/mcp", force=True, suspend=True), 0.1)
    assert result["stale"] and "缓存" in result["detail"]

@pytest.mark.asyncio
async def test_pause_control_is_immediate_and_slow_persistence_does_not_block_health(client, session, monkeypatch):
    import backend.main as api
    @contextmanager
    def slow_session():
        time.sleep(0.25)  # simulate a connection/WAL wait in the persistence thread
        yield session
    monkeypatch.setattr(api, "SessionLocal", slow_session)
    tasks = BackgroundTasks()
    started = time.monotonic()
    result = await api.pause(api.PauseInput(paused=True), tasks)
    assert time.monotonic() - started < 0.05
    assert result["paused"] and pause_requested()
    persistence = asyncio.create_task(tasks())
    await asyncio.sleep(0.01)
    assert (await asyncio.wait_for(api.health(), 0.05))["ok"]
    await persistence
    assert settings(session)["paused"]

@pytest.mark.asyncio
async def test_latest_pause_command_wins_even_when_background_tasks_arrive_out_of_order(client, session):
    import backend.main as api
    old, new = BackgroundTasks(), BackgroundTasks()
    await api.pause(api.PauseInput(paused=True), old)
    await api.pause(api.PauseInput(paused=False), new)
    await new()
    await old()
    assert not pause_requested() and not settings(session)["paused"]

@pytest.mark.asyncio
async def test_health_jobs_and_stop_remain_responsive_during_slow_platform_write(client, session, article_factory):
    import backend.main as api
    class SlowAdapter(FakeAdapter):
        started = asyncio.Event()
        release = asyncio.Event()
        publish_calls = 0
        async def publish(self, *args):
            self.started.set()
            await self.release.wait()
            return await super().publish(*args)
    article = article_factory()
    SlowAdapter.article = article
    SlowAdapter.persisted_new = False
    SlowAdapter.current_owner = "owner-1"
    _, job = ready(session, article)
    execution = asyncio.create_task(PublishingAgent(SlowAdapter).execute(session, job))
    await asyncio.wait_for(SlowAdapter.started.wait(), 0.5)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=api.app), base_url="http://test", trust_env=False) as http:
        health = await asyncio.wait_for(http.get("/api/health"), 0.3)
        jobs = await asyncio.wait_for(http.get("/api/jobs"), 0.3)
        stopped = await asyncio.wait_for(http.post("/api/publishing/pause", json={"paused": True}), 0.3)
        assert health.json()["ok"] and jobs.json()[0]["status"] == "PUBLISHING"
        assert stopped.json()["paused"]
    SlowAdapter.release.set()
    await asyncio.wait_for(execution, 0.5)
    assert settings(session)["paused"] and SlowAdapter.publish_calls == 1

def test_loopback_mcp_client_ignores_proxy_environment(monkeypatch):
    from backend.mcp import XiaohongshuMcpAdapter
    observed = {}
    def fake_client(**kwargs):
        observed.update(kwargs)
        return object()
    monkeypatch.setattr(httpx, "AsyncClient", fake_client)
    XiaohongshuMcpAdapter("http://127.0.0.1:18060/mcp")
    assert observed["trust_env"] is False

@pytest.mark.asyncio
async def test_console_status_returns_immediately_while_browser_read_is_slow(monkeypatch):
    import backend.main as api
    started, release = asyncio.Event(), asyncio.Event()
    calls = []
    async def slow_read(url, **kwargs):
        calls.append(url)
        started.set()
        await release.wait()
        return {"connected": True, "logged_in": True}
    monkeypatch.setattr(api, "mcp_health", slow_read)
    monkeypatch.setattr(api, "_health_task", None)
    monkeypatch.setattr(api, "_health_cache", {"at": 0, "url": "", "value": {}})
    first = api.cached_mcp_health("http://local/mcp")
    await asyncio.wait_for(started.wait(), 0.1)
    second = api.cached_mcp_health("http://local/mcp")
    assert first["stale"] and second["stale"] and len(calls) == 1
    release.set()
    await api._health_task
