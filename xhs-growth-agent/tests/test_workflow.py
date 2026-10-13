import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import httpx
import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
from backend.db import make_engine, migrate
from backend.models import *
from backend.service import *
from backend.service import authorize as core_authorize

def authorize(*args, **kwargs):
    """Unit fixtures provide explicit proof; HTTP tests exercise MCP account lookup."""
    return core_authorize(*args, **kwargs, verified_account={"id": "owner-1", "name": "test-owner", "verified": True})

class FakeAdapter:
    publish_calls = 0
    show_new = True
    fail = False
    article = None
    edit_during_health = None
    persisted_new = False
    override_desc = None
    current_owner = "owner-1"

    def __init__(self, url):
        self.published = False

    async def health(self):
        if self.edit_during_health:
            self.edit_during_health()
        return {"connected": True, "logged_in": True, "detail": "logged in", "tools": ["get_my_profile", "publish_content", "get_feed_detail"]}

    async def close(self):
        pass

    async def call(self, name, args=None):
        feeds = [{"id": "old-note", "noteCard": {"displayTitle": "旧笔记", "user": {"userId": self.current_owner}}}]
        if (self.published or self.persisted_new) and self.show_new:
            feeds.append({"id": "new-note", "xsecToken": "private-access-test", "noteCard": {"displayTitle": self.article.title, "user": {"userId": "owner-1"}}})
        return {"structuredContent": {"feeds": feeds}}

    async def publish(self, *args):
        type(self).publish_calls += 1
        type(self).persisted_new = True
        self.published = True
        if self.fail:
            raise httpx.ReadTimeout("unknown")
        return {"structuredContent": {"status": "发布完成"}}

    async def feed_detail(self, note_id, token):
        article = self.article
        return {"feed_id": note_id, "data": {"note": {"noteId": note_id, "title": article.title, "desc": self.override_desc or article.body + " #开发测试", "user": {"userId": "owner-1"}, "imageList": [{} for _ in article.media], "time": int(datetime.now(ZoneInfo("Asia/Shanghai")).timestamp() * 1000)}}}

@pytest.fixture(autouse=True)
def reset_fake():
    FakeAdapter.publish_calls = 0
    FakeAdapter.show_new = True
    FakeAdapter.fail = False
    FakeAdapter.edit_during_health = None
    FakeAdapter.persisted_new = False
    FakeAdapter.override_desc = None
    FakeAdapter.current_owner = "owner-1"

def ready(session, article):
    review_article(session, article, "approve", "test reviewer")
    authorize(session, article, f"授权发布：{article.id}：v{article.version}", "公开可见")
    FakeAdapter.article = article
    publisher = PublishingAgent(FakeAdapter)
    return publisher, publisher.enqueue(session, article, "live")

def test_migration_all_required_entities_and_restart(tmp_path):
    from sqlalchemy import inspect
    url = f"sqlite:///{tmp_path / 'persistent.db'}"
    engine = make_engine(url)
    migrate(engine)
    migrate(engine)
    expected = {"topics", "sources", "content_briefs", "articles", "article_versions", "media_assets", "quality_reviews", "approvals", "publish_jobs", "publish_attempts", "published_posts", "post_metrics_snapshots", "growth_experiments", "daily_reports", "agent_runs", "model_usage", "audit_logs", "schema_version"}
    assert expected <= set(inspect(engine).get_table_names())
    with sessionmaker(bind=engine)() as s:
        s.add(Setting(key="daily_limit", value=2)); s.commit()
    engine.dispose()
    with sessionmaker(bind=make_engine(url))() as s:
        assert settings(s)["daily_limit"] == 2

def test_v2_migrates_legacy_authorizations_and_revokes_unbound_proof(tmp_path):
    from sqlalchemy import text, inspect
    engine = make_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE publish_authorizations (id VARCHAR PRIMARY KEY, created_at VARCHAR, article_id VARCHAR, version INTEGER, content_hash VARCHAR, visibility VARCHAR, consumed BOOLEAN, valid BOOLEAN)"))
        connection.execute(text("INSERT INTO publish_authorizations VALUES ('old-auth', '2026-10-12', 'old-article', 1, 'hash', '公开可见', 0, 1)"))
    migrate(engine)
    migrate(engine)
    with sessionmaker(bind=engine)() as legacy_session:
        authorization = legacy_session.get(PublishAuthorization, "old-auth")
        assert authorization.account_id == "" and not authorization.valid
        assert legacy_session.execute(text("SELECT MAX(version) FROM schema_version")).scalar() == 3
    assert {"account_id", "account_name"} <= {c["name"] for c in inspect(engine).get_columns("publish_authorizations")}

@pytest.mark.asyncio
async def test_capacity_100_topics_50_articles(session, render_stub):
    research = await TopicResearchAgent().run(session, "mock", 100)
    assert research["count"] == 100
    assert ChiefEditorAgent().run(session, 50)["count"] == 50
    generated = await ContentWriterAgent().run(session, 50, "mock")
    assert generated["count"] == 50, generated
    assert len(set(generated["article_ids"])) == 50
    assert session.scalar(select(func.count()).select_from(Article)) == 50
    assert session.scalar(select(func.count()).select_from(MediaAsset)) == 200
    assert session.scalar(select(func.count()).select_from(ArticleVersion)) == 50
    assert all(a.mode == "mock" for a in session.scalars(select(Article)).all())
    assert all(a.status == "PENDING_REVIEW" for a in session.scalars(select(Article)).all())
    assert session.scalar(select(func.count()).select_from(PublishedPost)) == 0
    assert FakeAdapter.publish_calls == 0

@pytest.mark.asyncio
async def test_research_is_idempotent(session):
    assert (await TopicResearchAgent().run(session, "mock", 100))["count"] == 100
    assert (await TopicResearchAgent().run(session, "mock", 100))["count"] == 0

def test_quality_rejects_duplicate_text_and_image(session, article_factory):
    first = article_factory("独特主题甲")
    second = article_factory("独特主题乙")
    second.title, second.body = first.title, first.body
    quality_review(session, second)
    assert second.status == "QUALITY_REJECTED"
    assert any("相似度" in reason for reason in second.quality["risks"])
    second.body = "完全独立内容" * 30 + "AI辅助创作"
    second.media = [first.media[0]] + second.media[1:]
    quality_review(session, second)
    assert any("图片哈希" in reason for reason in second.quality["risks"])

def test_source_required_without_mandatory_prose_disclaimer(session, article_factory):
    article = article_factory()
    article.body = article.body.replace("AI辅助创作", "")
    quality_review(session, article)
    assert article.status == "PENDING_REVIEW" and article.ai_assisted
    article.sources = [{"title": "传闻", "url": "https://example.com", "verified": False}]
    quality_review(session, article)
    assert article.status == "QUALITY_REJECTED"
    assert any("可靠来源" in risk for risk in article.quality["risks"])

def test_review_edit_invalidates_authorization(session, article_factory):
    article = article_factory()
    ready(session, article)
    edit_article(session, article, {"title": "新标题检查"})
    assert article.version == 2
    assert article.status == "PENDING_REVIEW"
    assert not session.scalar(select(Approval)).valid
    assert not session.scalar(select(PublishAuthorization)).valid
    assert session.scalar(select(PublishJob)).status == "CANCELLED"
    with pytest.raises(WorkflowError):
        PublishingAgent().enqueue(session, article, "live")

def test_authorization_exact_version_and_visibility(session, article_factory):
    article = article_factory()
    review_article(session, article, "approve", "human")
    with pytest.raises(WorkflowError):
        authorize(session, article, "我同意", "公开可见")
    with pytest.raises(WorkflowError):
        authorize(session, article, f"授权发布：{article.id}：v1", "public")
    assert authorize(session, article, f"授权发布：{article.id}：v1", "公开可见")["version"] == 1

def test_unverified_account_cannot_authorize(session, article_factory):
    article = article_factory()
    review_article(session, article, "approve", "human")
    with pytest.raises(WorkflowError, match="核实"):
        core_authorize(session, article, f"授权发布：{article.id}：v1", "公开可见")

@pytest.mark.asyncio
async def test_authorization_binds_account_from_mcp_profile(session, article_factory):
    article = article_factory()
    review_article(session, article, "approve", "human")
    result = await authorize_with_account(session, article, f"授权发布：{article.id}：v1", "公开可见", FakeAdapter)
    assert result["account_id"] == "owner-1"
    assert session.scalar(select(PublishAuthorization)).account_id == "owner-1"
    log = session.scalar(select(AuditLog).where(AuditLog.action == "publish.authorized"))
    assert log.data["account_verification"] == "get_my_profile"

@pytest.mark.asyncio
async def test_mock_publish_has_no_platform_effect_and_keeps_authorization(session, article_factory):
    article = article_factory()
    publisher, _ = ready(session, article)
    job = publisher.enqueue(session, article, "mock")
    await publisher.execute(session, job)
    assert job.status == "MOCK_PUBLISHED"
    assert article.status == "SCHEDULED"
    assert not session.scalar(select(PublishAuthorization)).consumed
    assert FakeAdapter.publish_calls == 0
    assert publisher.enqueue(session, article, "mock").id == job.id

def test_mock_article_cannot_receive_live_authorization(session, article_factory):
    article = article_factory(mode="mock")
    review_article(session, article, "approve", "human")
    with pytest.raises(WorkflowError):
        authorize(session, article, f"授权发布：{article.id}：v1", "公开可见")

@pytest.mark.asyncio
async def test_live_success_requires_independent_content_verification(session, article_factory):
    article = article_factory()
    publisher, job = ready(session, article)
    await publisher.execute(session, job)
    assert job.status == article.status == "PUBLISHED"
    assert session.scalar(select(PublishedPost)).platform_id == "new-note"
    assert session.scalar(select(PublishAuthorization)).consumed
    assert session.scalar(select(PublishAttempt)).status == "VERIFIED"
    assert FakeAdapter.publish_calls == 1
    await publisher.execute(session, job)
    assert FakeAdapter.publish_calls == 1
    assert publisher.enqueue(session, article, "live").id == job.id

@pytest.mark.asyncio
async def test_verified_post_uses_platform_publication_time_not_verification_time(session, article_factory, monkeypatch):
    original = FakeAdapter.feed_detail
    async def earlier_platform_stamp(self, note_id, token):
        result = await original(self, note_id, token)
        result["data"]["note"]["time"] = int((datetime.now(ZoneInfo("Asia/Shanghai")).timestamp() - 60) * 1000)
        return result
    monkeypatch.setattr(FakeAdapter, "feed_detail", earlier_platform_stamp)
    article = article_factory()
    publisher, job = ready(session, article)
    await publisher.execute(session, job)
    post = session.scalar(select(PublishedPost))
    assert post and job.status == "PUBLISHED"
    assert (datetime.fromisoformat(post.verification["verified_at"]) - datetime.fromisoformat(post.published_at)).total_seconds() >= 50

@pytest.mark.asyncio
async def test_switched_login_account_is_blocked_and_paused_without_submission(session, article_factory):
    article = article_factory()
    publisher, job = ready(session, article)
    FakeAdapter.current_owner = "different-owner"
    await publisher.execute(session, job)
    assert job.status == "BLOCKED"
    assert "账号" in job.error
    assert settings(session)["paused"]
    assert FakeAdapter.publish_calls == 0
    authorization = session.scalar(select(PublishAuthorization))
    assert not authorization.valid and not authorization.consumed
    assert session.scalar(select(func.count()).select_from(PublishAttempt)) == 0

def test_title_and_cards_edit_regenerates_media_and_saves_actual_version(session, article_factory):
    article = article_factory()
    ready(session, article)
    old_hashes = [m["sha256"] for m in article.media]
    edit_article(session, article, {"title": "改写后的具体步骤", "body": article.body, "cards": [{"title": "新操作", "body": "新步骤一"}, {"title": "新检查", "body": "新步骤二"}], "template": "technology"})
    assert article.version == 2 and article.status == "PENDING_REVIEW"
    assert [m["sha256"] for m in article.media] != old_hashes
    version = session.scalar(select(ArticleVersion).where(ArticleVersion.article_id == article.id, ArticleVersion.version == 2))
    assert version.data["media"] == article.media
    assert version.data["cards"] == article.cards
    assert not session.scalar(select(Approval)).valid

@pytest.mark.asyncio
async def test_publish_completion_without_independent_post_is_unknown(session, article_factory):
    article = article_factory()
    FakeAdapter.show_new = False
    publisher, job = ready(session, article)
    await publisher.execute(session, job)
    assert job.status == article.status == "VERIFY_REQUIRED"
    assert settings(session)["paused"]
    assert session.scalar(select(func.count()).select_from(PublishedPost)) == 0
    await publisher.execute(session, job)
    assert FakeAdapter.publish_calls == 1

@pytest.mark.asyncio
async def test_read_only_reconciliation_can_confirm_delayed_result_without_reposting(session, article_factory):
    article = article_factory()
    FakeAdapter.show_new = False
    publisher, job = ready(session, article)
    await publisher.execute(session, job)
    assert job.status == "VERIFY_REQUIRED"
    FakeAdapter.show_new = True
    await publisher.verify(session, job)
    assert job.status == "PUBLISHED"
    assert FakeAdapter.publish_calls == 1
    assert settings(session)["paused"]  # does not silently override a human pause

@pytest.mark.asyncio
async def test_matching_title_with_wrong_body_is_not_publish_proof(session, article_factory):
    article = article_factory()
    FakeAdapter.override_desc = "另一个正文，不能认定是刚提交的内容"
    publisher, job = ready(session, article)
    await publisher.execute(session, job)
    assert job.status == "VERIFY_REQUIRED"
    assert session.scalar(select(func.count()).select_from(PublishedPost)) == 0

@pytest.mark.asyncio
async def test_timeout_after_submission_is_never_retried(session, article_factory):
    article = article_factory()
    FakeAdapter.fail = True
    publisher, job = ready(session, article)
    await publisher.execute(session, job)
    assert job.status == "VERIFY_REQUIRED"
    assert FakeAdapter.publish_calls == 1
    assert session.scalar(select(func.count()).select_from(PublishAttempt)) == 1
    await publisher.execute(session, job)
    assert FakeAdapter.publish_calls == 1

@pytest.mark.asyncio
async def test_pause_and_quota_gate(session, article_factory):
    article = article_factory()
    publisher, job = ready(session, article)
    save_settings(session, {"paused": True})
    await publisher.execute(session, job)
    assert job.status == "QUEUED" and FakeAdapter.publish_calls == 0
    save_settings(session, {"paused": False, "daily_limit": 0})
    await publisher.execute(session, job)
    assert job.status == "QUEUED" and FakeAdapter.publish_calls == 0

@pytest.mark.asyncio
async def test_pause_during_network_preflight_stops_submission(session, article_factory):
    article = article_factory()
    publisher, job = ready(session, article)
    FakeAdapter.edit_during_health = staticmethod(lambda: save_settings(session, {"paused": True}))
    await publisher.execute(session, job)
    assert FakeAdapter.publish_calls == 0
    assert job.status == "QUEUED"
    assert settings(session)["paused"]
    assert not session.scalar(select(PublishAuthorization)).consumed

@pytest.mark.asyncio
async def test_edit_during_network_preflight_invalidates_queued_submission(session, article_factory):
    article = article_factory()
    publisher, job = ready(session, article)
    FakeAdapter.edit_during_health = staticmethod(lambda: edit_article(session, article, {"title": "检查期间修改"}))
    await publisher.execute(session, job)
    assert job.status == "CANCELLED"
    assert FakeAdapter.publish_calls == 0
    assert not session.scalar(select(PublishAuthorization)).valid

def test_modified_image_invalidates_publish(session, article_factory):
    article = article_factory()
    review_article(session, article, "approve", "human")
    Path(article.media[0]["path"]).write_bytes(b"edited image")
    with pytest.raises(WorkflowError, match="图片文件已改变"):
        PublishingAgent().enqueue(session, article, "mock")

def test_crash_recovery_marks_unknown_and_pauses(session, article_factory):
    article = article_factory()
    _, job = ready(session, article)
    job.status = article.status = "PUBLISHING"
    session.add(PublishAttempt(job_id=job.id, request={"content_hash": job.content_hash}))
    session.commit()
    assert recover(session) == 1
    assert job.status == "VERIFY_REQUIRED" and settings(session)["paused"]
    assert recover(session) == 0

def test_report_does_not_invent_metrics(session, article_factory):
    article_factory()
    report = AnalyticsGrowthAgent().report(session)
    assert report["published"] == 0
    assert report["metrics"]["views"] is None
    assert report["metrics"]["likes"] is None
    assert report["uncertainty"]
    assert parse_count("1.2万") is None
    assert parse_count("1,234") == 1234

@pytest.mark.asyncio
async def test_live_model_missing_is_blocked(session, monkeypatch):
    monkeypatch.setattr("backend.model_client.cli_path", lambda: None)
    result = await ContentWriterAgent().run(session, 3, "live")
    assert result["count"] == 0 and result["blocked"]
    assert session.scalar(select(AgentRun)).status == "BLOCKED"
