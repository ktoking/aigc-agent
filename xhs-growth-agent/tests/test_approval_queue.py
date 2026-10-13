from contextlib import nullcontext
import pytest
from sqlalchemy import select, func
from backend.models import Article, Approval, PublishJob, PublishAuthorization, PublishAttempt, AgentRun, AuditLog, PublishedPost
from backend.service import settings, save_settings, set_approval_policy, review_article, enqueue_approved, queue_approved_article, edit_article, WorkflowError, PublishingAgent, profile_baseline
from backend.publishing_worker import PublishingWorker
from tests.test_workflow import FakeAdapter
from tests.test_api import client

@pytest.fixture(autouse=True)
def fake_reset():
    FakeAdapter.publish_calls = 0
    FakeAdapter.show_new = True
    FakeAdapter.fail = False
    FakeAdapter.edit_during_health = None
    FakeAdapter.persisted_new = False
    FakeAdapter.override_desc = None
    FakeAdapter.current_owner = "owner-1"

async def enable(session):
    return await set_approval_policy(session, True, FakeAdapter)

@pytest.mark.asyncio
async def test_explicit_enable_binds_verified_profile_and_approve_enqueues_once(session, article_factory):
    assert not settings(session)["approval_to_queue"]
    await enable(session)
    assert settings(session)["approved_account_id"] == "owner-1"
    article = article_factory()
    review_article(session, article, "approve", "human")
    assert article.status == "SCHEDULED"
    authorization = session.scalar(select(PublishAuthorization))
    assert authorization.policy == "approval_to_queue" and authorization.account_id == "owner-1"
    assert not authorization.consumed
    job = session.scalar(select(PublishJob))
    assert job.status == "QUEUED" and FakeAdapter.publish_calls == 0
    assert queue_approved_article(session, article).id == job.id
    assert session.scalar(select(func.count()).select_from(PublishJob)) == 1
    assert session.scalar(select(func.count()).select_from(PublishAuthorization)) == 1
    log = session.scalar(select(AuditLog).where(AuditLog.action == "publish.authorized"))
    assert "人工审批" in log.data["authority"]

@pytest.mark.asyncio
async def test_already_approved_batch_enqueues_real_articles_and_blocks_mock(session, article_factory):
    articles = [article_factory("MCP调用边界"), article_factory("日志来源怎么核对"), article_factory("Mock容量演示", "mock")]
    for article in articles:
        review_article(session, article, "approve", "human")
    await enable(session)
    result = enqueue_approved(session)
    assert result["count"] == 2 and len(result["blocked"]) == 1
    assert "Mock" in result["blocked"][0]["reason"]
    assert all(a.status == "SCHEDULED" for a in articles[:2])
    assert articles[2].status == "APPROVED"
    assert session.scalar(select(func.count()).select_from(PublishAuthorization)) == 2
    assert FakeAdapter.publish_calls == 0

@pytest.mark.asyncio
async def test_mock_approval_never_auto_authorizes_or_queues(session, article_factory):
    await enable(session)
    article = article_factory(mode="mock")
    review_article(session, article, "approve", "human")
    assert article.status == "APPROVED"
    assert session.scalar(select(func.count()).select_from(PublishAuthorization)) == 0
    assert session.scalar(select(func.count()).select_from(PublishJob)) == 0

@pytest.mark.asyncio
async def test_edit_invalidates_approval_policy_job_and_auth(session, article_factory):
    await enable(session)
    article = article_factory()
    review_article(session, article, "approve", "human")
    edit_article(session, article, {"body": article.body + " 人工补充新边界。"})
    assert article.version == 2 and article.status == "PENDING_REVIEW"
    assert not session.scalar(select(Approval)).valid
    assert not session.scalar(select(PublishAuthorization)).valid
    assert session.scalar(select(PublishJob)).status == "CANCELLED"
    with pytest.raises(WorkflowError):
        queue_approved_article(session, article)

@pytest.mark.asyncio
async def test_disabling_cancels_unsent_auto_job_and_reenable_reactivates_only_without_attempt(session, article_factory):
    await enable(session)
    article = article_factory()
    review_article(session, article, "approve", "human")
    job = session.scalar(select(PublishJob))
    old_authorization = job.authorization_id
    await set_approval_policy(session, False, FakeAdapter)
    assert job.status == "CANCELLED" and article.status == "APPROVED"
    assert settings(session)["paused"]
    assert not session.get(PublishAuthorization, old_authorization).valid
    await enable(session)
    reenqueued = queue_approved_article(session, article)
    assert reenqueued.id == job.id and reenqueued.status == "QUEUED"
    assert reenqueued.authorization_id != old_authorization
    assert session.scalar(select(func.count()).select_from(PublishJob)) == 1
    session.add(PublishAttempt(job_id=job.id, request={"test": True}))
    job.status = "CANCELLED"
    article.status = "APPROVED"
    session.commit()
    with pytest.raises(WorkflowError, match="提交记录"):
        queue_approved_article(session, article)

@pytest.mark.asyncio
async def test_approval_policy_never_follows_a_switched_account(session, article_factory):
    await enable(session)
    article = article_factory()
    review_article(session, article, "approve", "human")
    FakeAdapter.current_owner = "other-owner"
    worker = PublishingWorker(lambda: nullcontext(session), lambda: PublishingAgent(FakeAdapter))
    assert await worker.tick() == "BLOCKED"
    assert settings(session)["paused"]
    assert settings(session)["approved_account_id"] == "owner-1"
    assert FakeAdapter.publish_calls == 0

@pytest.mark.asyncio
async def test_worker_processes_once_without_scheduler_and_stops_on_unknown(session, article_factory):
    articles = [article_factory("MCP调用边界"), article_factory("日志来源怎么核对")]
    await enable(session)
    for article in articles:
        review_article(session, article, "approve", "human")
    FakeAdapter.article = articles[0]
    FakeAdapter.show_new = False
    worker = PublishingWorker(lambda: nullcontext(session), lambda: PublishingAgent(FakeAdapter))
    assert not settings(session)["scheduler_enabled"]
    assert await worker.tick() == "VERIFY_REQUIRED"
    assert await worker.tick() == "PAUSED"
    assert FakeAdapter.publish_calls == 1
    assert session.scalar(select(func.count()).select_from(PublishAttempt)) == 1
    assert session.scalar(select(func.count()).select_from(PublishJob).where(PublishJob.status == "QUEUED")) == 1

@pytest.mark.asyncio
async def test_worker_idle_pause_and_quota_do_not_write_runs_repeatedly(session, article_factory):
    worker = PublishingWorker(lambda: nullcontext(session), lambda: PublishingAgent(FakeAdapter))
    assert await worker.tick() == "IDLE"
    assert await worker.tick() == "IDLE"
    article = article_factory()
    await enable(session)
    review_article(session, article, "approve", "human")
    save_settings(session, {"paused": True})
    assert await worker.tick() == "PAUSED"
    save_settings(session, {"paused": False, "daily_limit": 0})
    assert await worker.tick() == "QUOTA_WAIT"
    assert await worker.tick() == "QUOTA_WAIT"
    assert session.scalar(select(func.count()).select_from(AgentRun)) == 0
    assert FakeAdapter.publish_calls == 0

@pytest.mark.asyncio
async def test_worker_lifecycle_recovers_queued_work_without_scheduler(session, article_factory):
    import asyncio
    await enable(session)
    article = article_factory()
    review_article(session, article, "approve", "human")
    FakeAdapter.article = article
    worker = PublishingWorker(lambda: nullcontext(session), lambda: PublishingAgent(FakeAdapter), interval=0.01)
    worker.start()
    for _ in range(100):
        await asyncio.sleep(0.005)
        if article.status == "PUBLISHED":
            break
    await worker.stop()
    assert article.status == "PUBLISHED"
    assert not settings(session)["scheduler_enabled"]
    assert FakeAdapter.publish_calls == 1
    assert session.scalar(select(func.count()).select_from(AgentRun)) == 1

def test_unverified_setting_id_cannot_replace_profile_identity():
    with pytest.raises(WorkflowError):
        profile_baseline({"feeds": []}, "fabricated-id")

def test_fast_review_api_auto_queue_without_confirmation(client, article_factory):
    article = article_factory()
    enabled = client.patch("/api/settings", json={"approval_to_queue": True, "approved_account_id": "untrusted-input"})
    assert enabled.status_code == 200 and enabled.json()["approved_account_id"] == "owner-1"
    response = client.post(f"/api/articles/{article.id}/review", json={"decision": "approve", "reviewer": "人工审批"})
    assert response.status_code == 200 and response.json()["status"] == "SCHEDULED"
    queued = client.post("/api/publishing/enqueue-approved", json={"article_ids": [article.id]})
    assert queued.status_code == 200 and queued.json()["count"] == 1
    assert FakeAdapter.publish_calls == 0
