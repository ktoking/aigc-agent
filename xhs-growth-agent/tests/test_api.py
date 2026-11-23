from fastapi.testclient import TestClient
from contextlib import nullcontext
import pytest
from backend.db import get_db
from backend.models import Article

@pytest.fixture
def client(session, monkeypatch):
    import backend.main as api
    async def status(*args, **kwargs):
        return {"connected": True, "logged_in": False, "detail": "test-only", "tools": []}
    monkeypatch.setattr(api, "mcp_health", status)
    monkeypatch.setattr(api, "migrate", lambda: None)
    monkeypatch.setattr(api, "SessionLocal", lambda: nullcontext(session))
    monkeypatch.setattr(api, "recover", lambda _session: 0)
    monkeypatch.setattr(api, "configure_scheduler", lambda _enabled: None)
    monkeypatch.setattr(api, "stop_scheduler", lambda: None)
    monkeypatch.setattr(api, "start_publishing_worker", lambda: None)
    monkeypatch.setattr(api, "wake_publishing_worker", lambda: None)
    async def no_worker_stop():
        pass
    monkeypatch.setattr(api, "stop_publishing_worker", no_worker_stop)
    async def verified_authorize(s, article, confirmation, visibility):
        from backend.service import authorize_with_account
        from tests.test_workflow import FakeAdapter
        FakeAdapter.persisted_new = False
        FakeAdapter.current_owner = "owner-1"
        FakeAdapter.article = article
        return await authorize_with_account(s, article, confirmation, visibility, FakeAdapter)
    monkeypatch.setattr(api, "authorize_with_account", verified_authorize)
    async def verified_policy(s, enabled):
        from backend.service import set_approval_policy
        from tests.test_workflow import FakeAdapter
        FakeAdapter.persisted_new = False
        FakeAdapter.current_owner = "owner-1"
        return await set_approval_policy(s, enabled, FakeAdapter)
    monkeypatch.setattr(api, "set_approval_policy", verified_policy)
    api.app.dependency_overrides[get_db] = lambda: session
    with TestClient(api.app, raise_server_exceptions=True) as value:
        yield value
    api.app.dependency_overrides.clear()

def test_review_authorize_and_mock_publish_api(client, article_factory):
    article = article_factory()
    article_id = article.id
    response = client.get("/api/articles")
    assert response.status_code == 200 and response.json()[0]["status"] == "PENDING_REVIEW"
    assert client.post(f"/api/articles/{article_id}/publish", json={"mode": "live"}).status_code == 409
    assert client.post(f"/api/articles/{article_id}/review", json={"decision": "approve", "reviewer": "人工测试"}).json()["status"] == "APPROVED"
    assert client.post(f"/api/articles/{article_id}/authorize", json={"confirmation": "随便确认", "visibility": "公开可见"}).status_code == 409
    authorized = client.post(f"/api/articles/{article_id}/authorize", json={"confirmation": f"授权发布：{article_id}：v1", "visibility": "公开可见"})
    assert authorized.status_code == 200 and not authorized.json()["consumed"]
    published = client.post(f"/api/articles/{article_id}/publish", json={"mode": "mock"})
    assert published.status_code == 200 and published.json()["status"] == "MOCK_PUBLISHED"
    assert client.get(f"/api/articles/{article_id}").json()["status"] == "APPROVED"
    assert client.get("/api/dashboard").json()["metrics"]["views"] is None

def test_request_bounds_and_malformed_edit(client, article_factory):
    article = article_factory()
    assert client.patch(f"/api/articles/{article.id}", json={"title": "很" * 21}).status_code == 422
    assert client.post("/api/generate", json={"count": 51}).status_code == 422
    assert client.patch("/api/settings", json={"quality_threshold": 20}).status_code == 422
    assert client.patch(f"/api/articles/{article.id}", json={"media_order": ["unknown"]}).status_code == 409
    assert client.get("/api/articles/missing").status_code == 404

def test_agent_revision_updates_entire_public_draft_and_preserves_internal_sources(client, session, article_factory, monkeypatch):
    from backend import main
    from backend.models import ArticleVersion, PublishJob
    from backend.service import save_settings
    from sqlalchemy import select
    article = article_factory()
    previous_cards, previous_media = article.cards, article.media
    sources = list(article.sources)
    draft = {"title": "买杯咖啡还要按人头收费？", "title_candidates": ["买杯咖啡还要按人头收费？", "喝杯咖啡，座位也成了门槛", "谁该替店里的规则买单"],
             "body": "如果两个人共饮一杯，却只能一个人坐下，这种规矩让我不舒服。" * 7,
             "tags": ["消费规则"], "cards": [{"title": "座位也成了消费门槛", "body": "一杯饮料为何还要区分谁能坐下？"}, {"title": "经营成本谁来承担", "body": "普通消费者的预算和陪伴需求也应该被看见。"}], "comment_prompt": "这种座位规则，你能接受吗？"}
    async def write(_self, _session, brief, _settings):
        assert brief["sources"] == sources
        assert brief["tones"] == ["objective", "gentle"]
        return draft
    monkeypatch.setattr(main.ModelClient, "write", write)
    save_settings(session, {"model_mode": "live"})
    response = client.post(f"/api/articles/{article.id}/revise", json={"instruction": "改成客观温和的表达，配图也一起改", "tones": ["objective", "gentle"]})
    assert response.status_code == 200
    value = response.json()
    assert value["version"] == 2 and value["status"] == "PENDING_REVIEW"
    for key in ("title", "body", "tags", "cards", "title_candidates", "comment_prompt"):
        assert value[key] == draft[key]
    assert value["sources"] == sources and value["media"] != previous_media
    old = session.scalar(select(ArticleVersion).where(ArticleVersion.article_id == article.id, ArticleVersion.version == 1))
    assert old.data["cards"] == previous_cards
    assert not session.scalars(select(PublishJob).where(PublishJob.article_id == article.id)).all()

def test_dashboard_contract_and_no_model_secrets(client, monkeypatch):
    monkeypatch.setenv("MODEL_API_KEY", "secret-test-value")
    monkeypatch.setenv("MODEL_BASE_URL", "http://test/v1")
    dashboard = client.get("/api/dashboard").json()
    assert {"counts", "agents", "mcp", "model", "paused", "daily_limit", "recent_runs", "metrics", "costs"} <= dashboard.keys()
    assert dashboard["model"]["configured"]
    assert len(dashboard["agents"]) == 7
    assert "secret-test-value" not in client.get("/api/settings").text
