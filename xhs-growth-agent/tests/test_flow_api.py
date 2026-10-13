import asyncio
import httpx
import pytest
from sqlalchemy import select, func
from backend.models import Article, PublishJob
from backend import main, creation, hotspots
from backend.db import get_db

@pytest.mark.asyncio
async def test_direction_submission_returns_before_model_and_reaches_review(session, render_stub, monkeypatch):
    started, release = asyncio.Event(), asyncio.Event()
    async def write(self, db, brief, config):
        assert brief['direction'] == '周末城市散步'
        started.set()
        await release.wait()
        return {'title': '周末散步准备清单', 'title_candidates': ['周末散步准备清单'] * 3,
                'body': '周末散步可以先确认路线、天气和体力安排。' * 12,
                'tags': ['周末', '散步'], 'cards': [{'title': '出发前', 'body': '留意天气'}, {'title': '安排路线', 'body': '适量步行'}]}
    monkeypatch.setattr(creation.ModelClient, 'write', write)
    main.app.dependency_overrides[get_db] = lambda: session
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://test') as client:
            invalid = await client.post('/api/creation/tasks', json={'direction': ''})
            assert invalid.status_code == 422
            response = await asyncio.wait_for(client.post('/api/creation/tasks', json={'direction': '周末城市散步'}), .5)
            assert response.status_code == 202 and response.json()['stage'] == 'QUEUED'
            task_id = response.json()['id']
            await asyncio.wait_for(started.wait(), .5)
            progress = await asyncio.wait_for(client.get('/api/creation/tasks/' + task_id), .5)
            assert progress.json()['stage'] == 'WRITING'
            release.set()
            await asyncio.wait_for(asyncio.gather(*creation._tasks), 2)
            final = (await client.get('/api/creation/tasks/' + task_id)).json()
            assert final['status'] == 'COMPLETED' and len(final['article_ids']) == 1
            session.expire_all()
            article = session.get(Article, final['article_ids'][0])
            assert article.status == 'PENDING_REVIEW' and article.category == '周末城市散步'
            assert session.scalar(select(func.count()).select_from(PublishJob)) == 0
    finally:
        release.set()
        main.app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_hotspot_query_keeps_direction_and_background_response(session, monkeypatch):
    release = asyncio.Event()
    async def collect(direction):
        assert direction == '旅行'
        await release.wait()
        return []
    monkeypatch.setattr(hotspots, 'collect_sources', collect)
    main.app.dependency_overrides[get_db] = lambda: session
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url='http://test') as client:
            response = await asyncio.wait_for(client.post('/api/hotspots/refresh', json={'direction': '旅行'}), .5)
            assert response.status_code == 202 and response.json()['direction'] == '旅行'
            read = await client.get('/api/hotspots?direction=旅行')
            assert read.json()['loading'] and read.json()['direction'] == '旅行'
            assert (await client.get('/api/hotspots')).json()['items'] == []
            release.set()
            await asyncio.gather(*hotspots._tasks.values())
            result = await client.get('/api/hotspots/tasks/' + response.json()['id'])
            assert result.json()['status'] == 'BLOCKED'
    finally:
        release.set()
        main.app.dependency_overrides.clear()
