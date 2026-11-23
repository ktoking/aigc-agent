import asyncio
from contextlib import asynccontextmanager
import os
import time
from typing import Literal
from urllib.parse import urlparse
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .config import DATA_DIR
from .db import migrate, SessionLocal, get_db
from .models import Article, Topic, AgentRun, ModelUsage, PublishJob, GrowthExperiment, Approval
from .mcp import XiaohongshuMcpAdapter, safe_data
from .model_client import ModelClient, model_status, ModelUnavailable
from .service import *
from .scheduler import configure_scheduler, stop_scheduler, execute_task
from .publishing_worker import start_publishing_worker, stop_publishing_worker, wake_publishing_worker
from .control import request_pause, pause_revision, persistence_lock
from . import creation, hotspots
from .tones import ToneName
from . import learning, writing_templates, writing_harness

_health_cache = {"at": 0, "url": "", "value": {"connected": False, "logged_in": False, "detail": "尚未检查 MCP", "tools": []}}
_health_lock = asyncio.Lock()
_health_task = None

def cached_mcp_health(url, suspend=False):
    """Console metadata must never wait for a browser navigation."""
    global _health_task
    cached = dict(_health_cache["value"]) if _health_cache["url"] == url else {"connected": False, "logged_in": False, "tools": [], "detail": "账号状态正在后台读取"}
    stale = _health_cache["url"] != url or time.monotonic() - _health_cache["at"] >= 15
    if suspend or PublishingAgent._lock.locked():
        return cached | {"stale": True, "detail": "发布排队、执行或核实期间暂停自动账号查询；显示最近缓存。"}
    if stale and not _health_lock.locked() and (_health_task is None or _health_task.done()):
        async def refresh():
            try:
                await mcp_health(url, force=True)
            except Exception:
                pass  # a failed read remains unknown; it never changes publication state
        _health_task = asyncio.create_task(refresh(), name="xhs-account-status")
    return cached | {"stale": stale}

async def mcp_health(url, force=False, suspend=False):
    # Polling health launches a real browser. Do not launch competing browsers during
    # a publication or an unresolved write, and do not let slow status refresh block UI controls.
    if suspend or PublishingAgent._lock.locked():
        cached = dict(_health_cache["value"]) if _health_cache["url"] == url else {"connected": False, "logged_in": False, "tools": []}
        return cached | {"stale": True, "detail": "发布排队、执行或核实期间暂停自动 MCP 状态查询；显示最近缓存，避免干扰浏览器。"}
    if _health_lock.locked() and not force:
        cached = dict(_health_cache["value"]) if _health_cache["url"] == url else {"connected": False, "logged_in": False, "tools": []}
        return cached | {"stale": True, "detail": "MCP 状态正在后台读取，当前显示缓存。"}
    async with _health_lock:
        if not force and _health_cache["url"] == url and time.monotonic() - _health_cache["at"] < 15:
            return _health_cache["value"]
        adapter = XiaohongshuMcpAdapter(url)
        try:
            value = await adapter.health()
            _health_cache.update(at=time.monotonic(), url=url, value=value)
            return value
        finally:
            await adapter.close()

@asynccontextmanager
async def lifespan(_app):
    migrate()
    with SessionLocal() as session:
        recover(session)
        learning.recover_learning(session)
        configure_scheduler(settings(session)["scheduler_enabled"])
    start_publishing_worker()
    yield
    await stop_publishing_worker()
    if _health_task and not _health_task.done():
        _health_task.cancel()
        try:
            await _health_task
        except asyncio.CancelledError:
            pass
    stop_scheduler()

app = FastAPI(title="XHS Growth Agent", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:18761", "http://localhost:18761"], allow_methods=["GET", "POST", "PATCH"], allow_headers=["Content-Type"])
(DATA_DIR / "media").mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=DATA_DIR / "media"), name="media")

@app.exception_handler(WorkflowError)
async def workflow_error(_request, error):
    return JSONResponse(status_code=409, content={"detail": str(error)})

@app.exception_handler(ModelUnavailable)
async def model_unavailable(_request, error):
    return JSONResponse(status_code=409, content={"detail": str(error), "status": "BLOCKED"})

@app.exception_handler(Exception)
async def unexpected_error(_request, error):
    return JSONResponse(status_code=500, content={"detail": f"执行失败：{type(error).__name__}；请查看本地运行状态，发布未知结果需要人工核实"})

TemplateName = Literal["auto", "bold", "sticky", "editorial", "receipt", "split", "ink", "minimal", "magazine", "technology", "data", "travel", "comparison", "guide", "opinion", "lifestyle"]

class CardInput(BaseModel):
    title: str = Field(min_length=1, max_length=90)
    body: str = Field(min_length=1, max_length=800)
    cover_subtitle: str | None = Field(default=None, max_length=160)

class EditInput(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=20)
    body: str | None = Field(default=None, min_length=1, max_length=1000)
    tags: list[str] | None = None
    title_candidates: list[str] | None = Field(default=None, min_length=3, max_length=3)
    comment_prompt: str | None = Field(default=None, max_length=300)
    media_order: list[str] | None = None
    cards: list[CardInput] | None = Field(default=None, min_length=1, max_length=5)
    template: TemplateName | None = None

class ReviewInput(BaseModel):
    decision: Literal["approve", "reject"]
    reviewer: str = Field(min_length=1, max_length=100)

class CreationInput(BaseModel):
    direction: str = Field(min_length=1, max_length=300)
    count: int = Field(default=1, ge=1, le=3)
    topic_ids: list[str] = Field(default_factory=list, max_length=5)
    material: str = Field(default="", max_length=10000)
    tones: list[ToneName] = Field(default_factory=lambda: ["natural"], max_length=4)
    template_id: str = Field(default="auto", max_length=80)

class LearningInput(BaseModel):
    keywords: list[str] = Field(default_factory=lambda: ["职场感悟", "消费体验"], min_length=1, max_length=4)
    target_samples: int = Field(default=20, ge=4, le=30)

class HotspotInput(BaseModel):
    direction: str = Field(default="", max_length=150)

class ReviseInput(BaseModel):
    instruction: str = Field(min_length=1, max_length=1000)
    tones: list[ToneName] = Field(default_factory=lambda: ["natural"], max_length=4)

class CoverInput(BaseModel):
    template: TemplateName = "auto"

class AuthorizationInput(BaseModel):
    confirmation: str
    visibility: str = "公开可见"

class PublishInput(BaseModel):
    mode: Literal["mock", "live"] = "mock"
    visibility: str | None = None

class ResearchInput(BaseModel):
    mode: Literal["mock", "live"] = "mock"
    count: int = Field(default=100, ge=1, le=100)
    keywords: list[str] | None = None

class PlanInput(BaseModel):
    mode: Literal["mock", "live"] | None = None
    limit: int = Field(default=50, ge=1, le=50)

class GenerateInput(BaseModel):
    count: int = Field(default=3, ge=1, le=50)
    mode: Literal["mock", "live"] = "mock"

class PauseInput(BaseModel):
    paused: bool

class EnqueueApprovedInput(BaseModel):
    article_ids: list[str] | None = Field(default=None, max_length=100)

class NoSubmissionInput(BaseModel):
    log_line: str = Field(min_length=30, max_length=1000)
    operator: str = Field(min_length=1, max_length=100)
    explanation: str = Field(min_length=20, max_length=2000)

class SettingsInput(BaseModel):
    daily_limit: int | None = Field(default=None, ge=0, le=50)
    quality_threshold: int | None = Field(default=None, ge=80, le=100)
    account_positioning: str | None = None
    model_mode: Literal["mock", "live"] | None = None
    mcp_url: str | None = None
    paused: bool | None = None
    scheduler_enabled: bool | None = None
    production_target: int | None = Field(default=None, ge=1, le=50)
    keywords: list[str] | None = None
    rss_urls: list[str] | None = None
    user_id: str | None = None
    model_name: Literal["gpt-6.1-sol"] | None = None
    model_provider: Literal["codex_cli"] | None = None
    model_reasoning_effort: Literal["high"] | None = None
    approval_to_queue: bool | None = None

def get_article(session, article_id):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(404, "文章不存在")
    return article

def suspend_mcp_poll(session, force=False):
    states = ["PUBLISHING", "VERIFY_REQUIRED"] + ([] if force else ["QUEUED"])
    return learning.reading(session) or bool(session.scalar(select(PublishJob.id).where(PublishJob.mode == "live", PublishJob.status.in_(states)).limit(1)))

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "xhs-growth-agent"}

@app.get("/api/dashboard")
async def dashboard(session: Session = Depends(get_db)):
    config = settings(session)
    counts = {"articles": session.scalar(select(func.count()).select_from(Article)), "topics": session.scalar(select(func.count()).select_from(Topic))}
    for key, state in (("pending_review", "PENDING_REVIEW"), ("approved", "APPROVED"), ("published", "PUBLISHED"), ("verify_required", "VERIFY_REQUIRED")):
        states = ["PENDING_REVIEW", "QUALITY_REJECTED"] if key == "pending_review" else [state]
        counts[key] = session.scalar(select(func.count()).select_from(Article).where(Article.status.in_(states)))
    recent = session.scalars(select(AgentRun).order_by(AgentRun.created_at.desc()).limit(20)).all()
    roles = []
    for name in AGENTS:
        aliases = {"Topic Research": [name, "Hotspot Refresh"], "Content Writer": [name, "Content Creation"]}.get(name, [name])
        last = session.scalar(select(AgentRun).where(AgentRun.name.in_(aliases)).order_by(AgentRun.created_at.desc()))
        roles.append({"name": name, "status": last.status if last else "IDLE", "last_run": last.created_at if last else None})
    usage = session.scalars(select(ModelUsage)).all()
    costs = [entry.cost_usd for entry in usage if entry.cost_usd is not None]
    return {"counts": counts, "agents": roles, "mcp": cached_mcp_health(config["mcp_url"], suspend=suspend_mcp_poll(session)), "model": {"mode": config["model_mode"], **model_status()}, "paused": config["paused"], "daily_limit": config["daily_limit"], "recent_runs": [serialize(r) for r in recent], "metrics": aggregate_metrics(session), "costs": {"calls": len(usage), "cost_usd": sum(costs) if len(costs) == len(usage) else None}}

@app.get("/api/articles")
def articles(session: Session = Depends(get_db)):
    return [safe_data(serialize(a)) for a in session.scalars(select(Article).order_by(Article.created_at.desc())).all()]

@app.post("/api/creation/tasks", status_code=202)
async def start_creation(data: CreationInput, session: Session = Depends(get_db)):
    return safe_data(await creation.start_task(session, data.direction, data.count, data.topic_ids, data.material, tones=data.tones, template_id=data.template_id))

@app.get("/api/writing/templates")
def writing_catalogue(tones: str = "natural", session: Session = Depends(get_db)):
    try:
        return {"items": writing_templates.catalogue(session, tones.split(",")), "learning": learning.latest(session), "harness": writing_harness.latest(session)}
    except ValueError as error:
        raise WorkflowError(str(error)) from None

@app.post("/api/writing/learn", status_code=202)
async def learn_writing(data: LearningInput, session: Session = Depends(get_db)):
    return await learning.start(session, data.keywords, target_samples=data.target_samples)

@app.get("/api/writing/harness")
def writing_harness_latest(session: Session = Depends(get_db)):
    return writing_harness.latest(session)

@app.get("/api/writing/learning/latest")
def writing_learning(session: Session = Depends(get_db)):
    return learning.latest(session)

@app.get("/api/creation/tasks/latest")
def latest_creation(session: Session = Depends(get_db)):
    return safe_data(creation.latest_task(session))

@app.get("/api/creation/tasks/{task_id}")
def creation_task(task_id: str, session: Session = Depends(get_db)):
    return safe_data(creation.get_task(session, task_id))

@app.get("/api/hotspots")
def read_hotspots(direction: str = "", session: Session = Depends(get_db)):
    return safe_data(hotspots.list_hotspots(session, direction))

@app.post("/api/hotspots/refresh", status_code=202)
async def refresh_hotspots(data: HotspotInput, session: Session = Depends(get_db)):
    return safe_data(await hotspots.start_refresh(session, data.direction))

@app.get("/api/hotspots/tasks/{task_id}")
def hotspot_task(task_id: str, session: Session = Depends(get_db)):
    return safe_data(hotspots.get_task(session, task_id))

@app.get("/api/articles/{article_id}")
def article(article_id: str, session: Session = Depends(get_db)):
    return safe_data(serialize(get_article(session, article_id)))

@app.patch("/api/articles/{article_id}")
def edit(article_id: str, data: EditInput, session: Session = Depends(get_db)):
    return serialize(edit_article(session, get_article(session, article_id), data.model_dump(exclude_none=True)))

@app.post("/api/articles/{article_id}/review")
async def review(article_id: str, data: ReviewInput, session: Session = Depends(get_db)):
    result = serialize(review_article(session, get_article(session, article_id), data.decision, data.reviewer))
    wake_publishing_worker()
    return result

@app.post("/api/articles/{article_id}/revise")
async def revise(article_id: str, data: ReviseInput, session: Session = Depends(get_db)):
    article = get_article(session, article_id)
    assert_editable(session, article)
    config = settings(session)
    if config["model_mode"] == "mock":
        raise WorkflowError("Mock 不会伪造智能改写；可直接编辑正文，或配置真实模型后要求 Agent 修改")
    version = article.version
    draft = await ModelClient().write(session, {"direction": article.category, "tones": data.tones, "content_kind": "source_based" if article.sources else "general_opinion", "original": {"title": article.title, "body": article.body}, "instruction": data.instruction, "sources": article.sources}, config)
    session.refresh(article)
    if article.version != version:
        raise WorkflowError("生成期间稿件已修改，请基于当前版本重新提出修改")
    return serialize(await asyncio.to_thread(edit_article, session, article, {key: draft[key] for key in ("title", "body", "tags", "cards", "title_candidates", "comment_prompt")}))

@app.post("/api/articles/{article_id}/cover")
def cover(article_id: str, data: CoverInput, session: Session = Depends(get_db)):
    article = get_article(session, article_id)
    assert_editable(session, article)
    snapshot(session, article)
    article.version += 1
    invalidate(session, article)
    render(session, article, data.template)
    quality_review(session, article)
    snapshot(session, article)
    session.commit()
    return serialize(article)

@app.post("/api/articles/{article_id}/authorize")
async def authorize_article(article_id: str, data: AuthorizationInput, session: Session = Depends(get_db)):
    return await authorize_with_account(session, get_article(session, article_id), data.confirmation, data.visibility)

@app.post("/api/articles/{article_id}/publish")
async def publish(article_id: str, data: PublishInput, session: Session = Depends(get_db)):
    publisher = PublishingAgent()
    job = publisher.enqueue(session, get_article(session, article_id), data.mode, data.visibility)
    await publisher.execute(session, job)
    return safe_data(serialize(job))

@app.get("/api/jobs")
def jobs(session: Session = Depends(get_db)):
    return [safe_data(serialize(j)) for j in session.scalars(select(PublishJob).order_by(PublishJob.created_at.desc())).all()]

@app.post("/api/jobs/{job_id}/verify")
async def verify_publish(job_id: str, session: Session = Depends(get_db)):
    job = session.get(PublishJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")
    return safe_data(serialize(await PublishingAgent().verify(session, job)))

@app.post("/api/publishing/pause")
async def pause(data: PauseInput, background: BackgroundTasks):
    revision = request_pause(data.paused)
    wake_publishing_worker()
    def persist():
        with persistence_lock:
            if revision != pause_revision():
                return  # a later stop/resume command superseded this background persistence
            with SessionLocal() as session:
                row = session.get(Setting, "paused")
                if row:
                    row.value = data.paused
                else:
                    session.add(Setting(key="paused", value=data.paused))
                audit(session, "publishing.pause", "system", {"paused": data.paused, "control_revision": revision})
                session.commit()
    background.add_task(persist)
    return {"paused": data.paused, "persistence": "pending"}

@app.post("/api/jobs/{job_id}/resolve-not-submitted")
def resolve_no_submission(job_id: str, data: NoSubmissionInput, session: Session = Depends(get_db)):
    job = session.get(PublishJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")
    return safe_data(serialize(PublishingAgent().resolve_not_submitted(session, job, data.log_line, data.operator, data.explanation)))

@app.post("/api/jobs/{job_id}/retry-pre-submit")
async def retry_pre_submit(job_id: str, session: Session = Depends(get_db)):
    job = session.get(PublishJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")
    result = await PublishingAgent().retry_pre_submit(session, job)
    return safe_data(serialize(result))  # remains paused until the operator resumes

@app.post("/api/publishing/enqueue-approved")
async def enqueue_approved_articles(data: EnqueueApprovedInput, session: Session = Depends(get_db)):
    result = enqueue_approved(session, data.article_ids)
    wake_publishing_worker()
    return result

@app.get("/api/topics")
def topics(session: Session = Depends(get_db)):
    return [safe_data(serialize(t)) for t in session.scalars(select(Topic).order_by(Topic.score.desc(), Topic.created_at.desc())).all()]

@app.post("/api/research")
async def research(data: ResearchInput, session: Session = Depends(get_db)):
    return await TopicResearchAgent().run(session, data.mode, data.count, data.keywords)

@app.post("/api/plan")
async def plan(data: PlanInput, session: Session = Depends(get_db)):
    if (data.mode or settings(session)["model_mode"]) == "live":
        return await ChiefEditorAgent().run_live(session, data.limit)
    return ChiefEditorAgent().run(session, data.limit)

@app.post("/api/generate")
async def generate(data: GenerateInput, session: Session = Depends(get_db)):
    return await ContentWriterAgent().run(session, data.count, data.mode)

@app.post("/api/demo")
def demo_articles(session: Session = Depends(get_db)):
    return demo(session)

@app.get("/api/settings")
def get_settings(session: Session = Depends(get_db)):
    return settings(session)

@app.patch("/api/settings")
async def update_settings(data: SettingsInput, session: Session = Depends(get_db)):
    patch = data.model_dump(exclude_none=True)
    if patch.get("mcp_url"):
        parsed = urlparse(patch["mcp_url"])
        if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
            raise WorkflowError("MCP URL 需要 HTTP/HTTPS，禁止在 URL 携带账号或密钥")
    if "approval_to_queue" in patch:
        enabled = patch.pop("approval_to_queue")
        await set_approval_policy(session, enabled)
        if not enabled:
            patch["paused"] = True
    result = save_settings(session, patch)
    if "scheduler_enabled" in patch:
        configure_scheduler(patch["scheduler_enabled"])
    wake_publishing_worker()
    return result

@app.get("/api/mcp/status")
async def mcp_status(refresh: bool = False, session: Session = Depends(get_db)):
    url = settings(session)["mcp_url"]
    suspend = suspend_mcp_poll(session, refresh)
    return await mcp_health(url, True, suspend=suspend) if refresh else cached_mcp_health(url, suspend=suspend)

@app.post("/api/mcp/qrcode")
async def qrcode(session: Session = Depends(get_db)):
    adapter = XiaohongshuMcpAdapter(settings(session)["mcp_url"])
    try:
        return await adapter.qrcode()
    except Exception as error:
        raise WorkflowError("二维码获取失败：" + type(error).__name__)
    finally:
        await adapter.close()

@app.get("/api/report")
def report(session: Session = Depends(get_db)):
    return AnalyticsGrowthAgent().report(session)

@app.post("/api/metrics/collect")
async def metrics(session: Session = Depends(get_db)):
    return await AnalyticsGrowthAgent().collect(session)

@app.get("/api/runs")
def runs(session: Session = Depends(get_db)):
    return [serialize(run) for run in session.scalars(select(AgentRun).order_by(AgentRun.created_at.desc()).limit(100)).all()]

@app.post("/api/scheduler/{task}/run")
async def scheduler_task(task: str):
    return await execute_task(task)

@app.get("/api/experiments")
def experiments(session: Session = Depends(get_db)):
    return [serialize(e) for e in session.scalars(select(GrowthExperiment)).all()]
