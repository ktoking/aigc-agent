from pathlib import Path
from contextlib import nullcontext
import pytest
from sqlalchemy import select, func
from backend.models import PublishAttempt, PublishJob, AuditLog, PublishAuthorization
from backend.service import PublishingAgent, WorkflowError, save_settings, settings
from tests.test_workflow import FakeAdapter, ready

@pytest.fixture
def failed_creator(session, article_factory, monkeypatch, tmp_path):
    import backend.service as service
    FakeAdapter.publish_calls = 0
    FakeAdapter.persisted_new = False
    FakeAdapter.current_owner = "owner-1"
    FakeAdapter.edit_during_health = None
    FakeAdapter.fail = False
    FakeAdapter.show_new = True
    article = article_factory()
    publisher, job = ready(session, article)
    job.status = article.status = "VERIFY_REQUIRED"
    job.error = "平台提交后发生 McpError，结果未知；禁止自动重试"
    auth = session.get(PublishAuthorization, job.authorization_id)
    auth.consumed = True
    attempt = PublishAttempt(job_id=job.id, request={}, status="VERIFY_REQUIRED")
    session.add(attempt)
    save_settings(session, {"paused": True, "approval_to_queue": True, "approved_account_id": "owner-1", "approved_account_name": "test-owner", "approved_account_verified_at": "verified"})
    session.commit()
    line = f'time="{attempt.created_at}" level=error msg="发布内容失败: title={article.title} 创作者中心登录失效，请重新扫码登录"'
    folder = tmp_path / ".runtime/logs"
    folder.mkdir(parents=True)
    (folder / "mcp.log").write_text(line + "\n")
    monkeypatch.setattr(service, "ROOT", tmp_path)
    return publisher, job, article, attempt, line

def resolve(session, failed):
    publisher, job, article, attempt, line = failed
    publisher.resolve_not_submitted(session, job, line, "test operator", "已核验原生源码：错误只在发布页初始化中抛出，早于图片上传与 Publish 调用。")
    return publisher, job, article, attempt

def test_resolution_preserves_history_and_pause(session, failed_creator):
    _, job, article, attempt = resolve(session, failed_creator)
    assert job.status == attempt.status == "NO_SUBMISSION"
    assert article.status == "APPROVED" and settings(session)["paused"]
    assert session.scalar(select(func.count()).select_from(PublishAttempt)) == 1
    assert attempt.response["resolution"]["job_id"] == job.id
    assert session.scalar(select(AuditLog).where(AuditLog.action == "publish.operator_resolved_no_submission"))

def test_timeout_or_missing_note_is_not_evidence(session, failed_creator):
    publisher, job, _, _, line = failed_creator
    job.error = "平台提交后发生 ReadTimeout，结果未知"
    with pytest.raises(WorkflowError, match="超时不能"):
        publisher.resolve_not_submitted(session, job, line, "operator", "没有在主页找到笔记所以想重发；这不能作为未提交证明。")
    assert job.status == "VERIFY_REQUIRED"

def test_unmatched_native_log_cannot_resolve(session, failed_creator):
    publisher, job, _, _, line = failed_creator
    with pytest.raises(WorkflowError):
        publisher.resolve_not_submitted(session, job, line.replace("创作者中心", "主页"), "operator", "这是并未出现在原生日志中的猜测，系统应拒绝处理。")
    assert job.status == "VERIFY_REQUIRED"

@pytest.mark.asyncio
async def test_single_recovery_retains_approval_and_excludes_only_proven_no_submission(session, failed_creator):
    publisher, original, article, attempt = resolve(session, failed_creator)
    retry = await publisher.retry_pre_submit(session, original)
    again = await publisher.retry_pre_submit(session, original)
    assert retry.id == again.id and retry.id != original.id
    assert retry.status == "QUEUED" and settings(session)["paused"]
    assert retry.version == original.version and retry.content_hash == original.content_hash
    assert session.scalar(select(func.count()).select_from(PublishJob)) == 2
    assert FakeAdapter.publish_calls == 0
    save_settings(session, {"paused": False, "daily_limit": 1})
    from backend.publishing_worker import PublishingWorker
    worker = PublishingWorker(lambda: nullcontext(session), lambda: publisher)
    assert await worker.tick() == "PUBLISHED"
    assert retry.status == "PUBLISHED" and FakeAdapter.publish_calls == 1
    assert attempt.status == "NO_SUBMISSION"
    save_settings(session, {"paused": True})
    assert (await publisher.retry_pre_submit(session, original)).id == retry.id
    assert FakeAdapter.publish_calls == 1

@pytest.mark.asyncio
async def test_recovery_rejects_account_change_and_edited_content(session, failed_creator):
    publisher, original, article, _ = resolve(session, failed_creator)
    FakeAdapter.current_owner = "other-owner"
    with pytest.raises(WorkflowError, match="账号"):
        await publisher.retry_pre_submit(session, original)
    FakeAdapter.current_owner = "owner-1"
    article.body += "changed"
    with pytest.raises(WorkflowError, match="变化"):
        await publisher.retry_pre_submit(session, original)
    assert FakeAdapter.publish_calls == 0
