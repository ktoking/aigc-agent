import json
from pathlib import Path
import subprocess
import pytest
from sqlalchemy import select
from backend import model_client as model
from backend.models import ModelUsage, Topic, ContentBrief, AgentRun
from backend.service import ChiefEditorAgent, settings, save_settings, WorkflowError

ARTICLE = {"title": "把Codex验收写清楚", "title_candidates": ["验收写清楚", "任务前列好检查项", "Codex任务的验收清单"], "body": "把实际问题写进任务，再把验收条件拆成能检查的结果。" * 8, "tags": ["Codex"], "cards": [{"title": "目标", "body": "明确预期结果"}], "comment_prompt": "你通常怎么写验收？"}

def fake_cli(monkeypatch, result=ARTICLE, exit_code=0, usage=True):
    captured = {}
    monkeypatch.setattr(model, "cli_path", lambda: "/official/codex")
    class Process:
        pid = 999999
        returncode = exit_code
        def __init__(self, args, **kwargs):
            captured.update(args=args, **kwargs)
            self.output = Path(args[args.index("--output-last-message") + 1])
        def communicate(self, payload=None, timeout=None):
            captured["prompt"] = payload
            self.output.write_text(json.dumps(result))
            event = {"type": "turn.completed", "usage": {"input_tokens": 17, "output_tokens": 31, "cached_input_tokens": 0}} if usage else {"type": "other"}
            return json.dumps(event).encode(), b"sensitive-error-not-for-output"
    monkeypatch.setattr(model.subprocess, "Popen", Process)
    return captured

@pytest.mark.asyncio
async def test_cli_is_fixed_and_isolated_and_records_measured_usage(session, monkeypatch):
    monkeypatch.setenv("MODEL_API_KEY", "never-inherit")
    monkeypatch.setenv("OPENAI_API_KEY", "never-inherit")
    monkeypatch.setenv("HTTPS_PROXY", "never-inherit")
    monkeypatch.setenv("CODEX_THREAD_ID", "never-inherit")
    captured = fake_cli(monkeypatch)
    client = model.ModelClient()
    assert await client.write(session, {"sources": []}, {}) == ARTICLE
    assert not any(key in captured["env"] for key in ["MODEL_API_KEY", "OPENAI_API_KEY", "HTTPS_PROXY", "CODEX_THREAD_ID"])
    args = captured["args"]
    for flag in ["--ignore-user-config", "--ignore-rules", "--ephemeral", "--skip-git-repo-check"]:
        assert flag in args
    assert args[args.index("--model") + 1] == "gpt-6.1-sol"
    assert 'model_reasoning_effort="high"' in args
    assert 'model_provider="openai"' in args
    assert "features.shell_tool=false" in args and "mcp_servers={}" in args
    assert captured["cwd"] != str(Path.cwd())
    assert captured["prompt"] and args[-1] == "-"
    usage = session.scalar(select(ModelUsage))
    assert usage.input_tokens == 17 and usage.output_tokens == 31 and usage.cost_usd is None
    assert client.last_metadata["tool_calls"] == 0

@pytest.mark.asyncio
async def test_cli_auth_failure_blocks_without_raw_error(session, monkeypatch):
    fake_cli(monkeypatch, exit_code=1, usage=False)
    with pytest.raises(model.ModelUnavailable) as error:
        await model.ModelClient().write(session, {}, {})
    assert "sensitive-error" not in str(error.value)
    assert "CLI_FAILED" in str(error.value)
    assert not session.scalars(select(ModelUsage)).all()

@pytest.mark.asyncio
async def test_cli_rejects_malformed_shape_and_length(session, monkeypatch):
    fake_cli(monkeypatch, result={"title": "bad"})
    with pytest.raises(model.ModelUnavailable):
        await model.ModelClient().write(session, {}, {})
    fake_cli(monkeypatch, result=ARTICLE | {"body": "too short"})
    with pytest.raises(model.ModelUnavailable):
        await model.ModelClient().write(session, {}, {})

@pytest.mark.asyncio
async def test_rank_cannot_omit_or_repeat_candidates(session, monkeypatch):
    fake_cli(monkeypatch, result={"evaluations": [{"index": 0, "score": 81, "reasons": ["明确"], "angle": "步骤"}]})
    with pytest.raises(model.ModelUnavailable):
        await model.ModelClient().rank(session, [{"title": "一"}, {"title": "二"}], {"account_positioning": "技术"})

@pytest.mark.asyncio
async def test_live_planning_uses_cli_and_preserves_trusted_sources(session, monkeypatch):
    topic = Topic(title="具体问题", category="Codex", score=80, reasons=[], sources=[{"url": "https://example.com/docs", "verified": True}], fingerprint="unique", mode="live", evidence={"source": "rss"})
    session.add(topic); session.commit()
    fake_cli(monkeypatch, result={"plans": [{"topic_id": topic.id, "title": "具体操作", "target_user": "开发者", "core_view": "可验证步骤", "keywords": ["Codex"], "style": "实操", "image_needs": "三张信息卡"}]})
    result = await ChiefEditorAgent().run_live(session, 1)
    assert result["count"] == 1
    brief = session.scalar(select(ContentBrief))
    assert brief.data["sources"] == topic.sources
    assert brief.data["model"] == "gpt-6.1-sol"
    assert session.scalar(select(ModelUsage)).agent == "Chief Editor"

@pytest.mark.asyncio
async def test_cli_missing_does_not_fall_back_to_api(session, monkeypatch):
    monkeypatch.setattr(model, "cli_path", lambda: None)
    monkeypatch.setenv("MODEL_API_KEY", "available-external-api-key")
    assert not model.configured()
    result = await ChiefEditorAgent().run_live(session, 1)
    assert result["count"] == 0 and result["blocked"]
    assert session.scalar(select(AgentRun)).status == "BLOCKED"

def test_provider_cannot_be_overridden(session):
    assert settings(session)["model_provider"] == "codex_cli"
    with pytest.raises(WorkflowError):
        save_settings(session, {"model_name": "other-model"})
    with pytest.raises(WorkflowError):
        save_settings(session, {"model_provider": "other-provider"})

@pytest.mark.asyncio
async def test_live_writer_selects_live_brief_past_old_mock_briefs(session, monkeypatch, render_stub):
    from backend.service import ContentWriterAgent
    mock_topic = Topic(title="旧Mock", category="测试", score=80, reasons=[], sources=[], fingerprint="mock-old", mode="mock", evidence={})
    live_topic = Topic(title="真实选题", category="Codex", score=80, reasons=[], sources=[{"url":"https://example.com/docs","verified":True}], fingerprint="live-new", mode="live", evidence={})
    session.add_all([mock_topic, live_topic]); session.commit()
    old = ContentBrief(topic_id=mock_topic.id, data={"sources": []})
    fresh = ContentBrief(topic_id=live_topic.id, data={"sources": live_topic.sources})
    session.add_all([old, fresh]); session.commit()
    fake_cli(monkeypatch)
    result = await ContentWriterAgent().run(session, 1, "live")
    assert result["count"] == 1
    assert fresh.status == "GENERATED" and old.status == "PLANNED"

def test_cli_timeout_kills_own_process_group(monkeypatch):
    captured = fake_cli(monkeypatch)
    class HungProcess:
        pid = 123456
        returncode = None
        calls = 0
        def __init__(self, *_args, **_kwargs):
            pass
        def communicate(self, *_args, **_kwargs):
            self.calls += 1
            if self.calls == 1:
                raise subprocess.TimeoutExpired("codex", 30)
            return b"", b""
    monkeypatch.setattr(model.subprocess, "Popen", HungProcess)
    killed=[]
    monkeypatch.setattr(model.os, "killpg", lambda pid, sig: killed.append((pid, sig)))
    with pytest.raises(model.ModelUnavailable, match="超时"):
        model.invoke_cli("只写内容", model.WRITE_SCHEMA)
    assert killed[0][0] == 123456

@pytest.mark.asyncio
async def test_unknown_usage_is_explicitly_null_in_audit_and_cost(session, monkeypatch):
    from backend.models import AuditLog
    fake_cli(monkeypatch, usage=False)
    client=model.ModelClient()
    await client.write(session, {}, {})
    assert client.last_metadata["usage"] is None
    audit=session.scalar(select(AuditLog).where(AuditLog.action == "model.call"))
    assert audit.data["usage"] is None and audit.data["cost_usd"] is None
    assert session.scalar(select(ModelUsage)).cost_usd is None

@pytest.mark.parametrize('message,code', [
    ('HTTP 401 unauthorized bearer-secret', 'AUTH'),
    ('You have hit your usage limit. retry 429', 'RATE_LIMIT'),
    ('Model gpt-6.1-sol is not available for this account', 'MODEL_ACCESS'),
    ('stream disconnected: error sending request https://private/?token=secret', 'NETWORK'),
    ("unexpected argument '--removed' found", 'CONFIG'),
    ('HTTP 503 service unavailable', 'UPSTREAM'),
    ('unclassified secret message', 'CLI_FAILED'),
])
@pytest.mark.asyncio
async def test_failed_turn_is_classified_and_audited_without_secrets(session, monkeypatch, message, code):
    from backend.models import AuditLog
    monkeypatch.setattr(model, 'cli_path', lambda: '/official/codex')
    class Failed:
        returncode = 1
        def __init__(self, *args, **kwargs): pass
        def communicate(self, *args, **kwargs):
            return json.dumps({'type':'turn.failed', 'error':{'message':message}}).encode(), b'credential-private-secret'
    monkeypatch.setattr(model.subprocess, 'Popen', Failed)
    with pytest.raises(model.ModelUnavailable) as error:
        await model.ModelClient().write(session, {}, {})
    audit = session.scalar(select(AuditLog).where(AuditLog.action == 'model.call'))
    assert audit.data['failure_code'] == code
    assert audit.data['usage'] is None and audit.data['exit_code'] == 1
    assert not session.scalars(select(ModelUsage)).all()
    assert 'secret' not in str(error.value) + json.dumps(audit.data)
    assert message not in json.dumps(audit.data)


def test_failed_turn_cannot_accept_result_even_with_zero_exit(monkeypatch):
    captured = fake_cli(monkeypatch)
    previous = model.subprocess.Popen
    class FailedTurn(previous):
        def communicate(self, *args, **kwargs):
            output, stderr = super().communicate(*args, **kwargs)
            return output + b'\n{"type":"turn.failed","error":{"message":"network connection interrupted"}}', stderr
    monkeypatch.setattr(model.subprocess, 'Popen', FailedTurn)
    with pytest.raises(model.ModelUnavailable) as error:
        model.invoke_cli('content', model.WRITE_SCHEMA)
    assert error.value.metadata['failure_code'] == 'NETWORK'
