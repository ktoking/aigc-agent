from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo
from sqlalchemy import JSON, Boolean, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def now():
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat()

def uid():
    return uuid4().hex

class Record:
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    created_at: Mapped[str] = mapped_column(String, default=now)

class Topic(Record, Base):
    __tablename__ = "topics"
    title: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String, default="AI 与开发技术")
    score: Mapped[int] = mapped_column(Integer, default=0)
    reasons: Mapped[list] = mapped_column(JSON, default=list)
    sources: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String, default="DISCOVERED")
    fingerprint: Mapped[str] = mapped_column(String, unique=True)
    mode: Mapped[str] = mapped_column(String, default="mock")
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)

class Source(Record, Base):
    __tablename__ = "sources"
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    retrieved_at: Mapped[str | None] = mapped_column(String, nullable=True)
    credibility: Mapped[str] = mapped_column(String, default="unverified")
    details: Mapped[dict] = mapped_column(JSON, default=dict)

class ContentBrief(Record, Base):
    __tablename__ = "content_briefs"
    topic_id: Mapped[str] = mapped_column(String, unique=True)
    data: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String, default="PLANNED")

class Article(Record, Base):
    __tablename__ = "articles"
    topic_id: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String)
    title_candidates: Mapped[list] = mapped_column(JSON, default=list)
    body: Mapped[str] = mapped_column(Text)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String, default="GENERATED")
    category: Mapped[str] = mapped_column(String, default="AI 与开发技术")
    style: Mapped[str] = mapped_column(String, default="技术实操教程")
    ai_assisted: Mapped[bool] = mapped_column(Boolean, default=True)
    sources: Mapped[list] = mapped_column(JSON, default=list)
    media: Mapped[list] = mapped_column(JSON, default=list)
    cards: Mapped[list] = mapped_column(JSON, default=list)
    quality: Mapped[dict] = mapped_column(JSON, default=dict)
    version: Mapped[int] = mapped_column(Integer, default=1)
    comment_prompt: Mapped[str] = mapped_column(String, default="")
    mode: Mapped[str] = mapped_column(String, default="mock")
    fingerprint: Mapped[str] = mapped_column(String)

class ArticleVersion(Record, Base):
    __tablename__ = "article_versions"
    __table_args__ = (UniqueConstraint("article_id", "version"),)
    article_id: Mapped[str] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)
    data: Mapped[dict] = mapped_column(JSON)
    content_hash: Mapped[str] = mapped_column(String)

class MediaAsset(Record, Base):
    __tablename__ = "media_assets"
    article_id: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    sha256: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    license: Mapped[str] = mapped_column(String)

class QualityReview(Record, Base):
    __tablename__ = "quality_reviews"
    article_id: Mapped[str] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)
    reasons: Mapped[list] = mapped_column(JSON)
    risks: Mapped[list] = mapped_column(JSON)

class Approval(Record, Base):
    __tablename__ = "approvals"
    article_id: Mapped[str] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)
    reviewer: Mapped[str] = mapped_column(String)
    decision: Mapped[str] = mapped_column(String)
    content_hash: Mapped[str] = mapped_column(String)
    valid: Mapped[bool] = mapped_column(Boolean, default=True)

class PublishAuthorization(Record, Base):
    __tablename__ = "publish_authorizations"
    article_id: Mapped[str] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String)
    visibility: Mapped[str] = mapped_column(String)
    account_id: Mapped[str] = mapped_column(String, default="")
    account_name: Mapped[str] = mapped_column(String, default="")
    policy: Mapped[str] = mapped_column(String, default="manual")
    consumed: Mapped[bool] = mapped_column(Boolean, default=False)
    valid: Mapped[bool] = mapped_column(Boolean, default=True)

class PublishJob(Record, Base):
    __tablename__ = "publish_jobs"
    article_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="QUEUED")
    mode: Mapped[str] = mapped_column(String)
    visibility: Mapped[str] = mapped_column(String, default="公开可见")
    authorization_id: Mapped[str | None] = mapped_column(String, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    response: Mapped[dict] = mapped_column(JSON, default=dict)
    idempotency_key: Mapped[str] = mapped_column(String, unique=True)

class PublishAttempt(Record, Base):
    __tablename__ = "publish_attempts"
    job_id: Mapped[str] = mapped_column(String, unique=True)
    request: Mapped[dict] = mapped_column(JSON)
    response: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String, default="STARTED")

class PublishedPost(Record, Base):
    __tablename__ = "published_posts"
    article_id: Mapped[str] = mapped_column(String, unique=True)
    job_id: Mapped[str] = mapped_column(String, unique=True)
    platform_id: Mapped[str] = mapped_column(String, unique=True)
    xsec_token: Mapped[str | None] = mapped_column(String, nullable=True)
    published_at: Mapped[str] = mapped_column(String, default=now)
    verification: Mapped[dict] = mapped_column(JSON, default=dict)

class PostMetricsSnapshot(Record, Base):
    __tablename__ = "post_metrics_snapshots"
    post_id: Mapped[str] = mapped_column(String)
    metrics: Mapped[dict] = mapped_column(JSON)
    age_hours: Mapped[float] = mapped_column(Float, default=0)
    window: Mapped[str] = mapped_column(String, default="current")
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)

class GrowthExperiment(Record, Base):
    __tablename__ = "growth_experiments"
    title: Mapped[str] = mapped_column(String)
    old_strategy: Mapped[dict] = mapped_column(JSON, default=dict)
    new_strategy: Mapped[dict] = mapped_column(JSON, default=dict)
    rationale: Mapped[str] = mapped_column(Text)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String, default="PLANNED")

class DailyReport(Record, Base):
    __tablename__ = "daily_reports"
    date: Mapped[str] = mapped_column(String, unique=True)
    data: Mapped[dict] = mapped_column(JSON)

class AgentRun(Record, Base):
    __tablename__ = "agent_runs"
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="RUNNING")
    mode: Mapped[str] = mapped_column(String, default="mock")
    finished_at: Mapped[str | None] = mapped_column(String, nullable=True)
    result: Mapped[dict] = mapped_column(JSON, default=dict)

class ModelUsage(Record, Base):
    __tablename__ = "model_usage"
    agent: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    mode: Mapped[str] = mapped_column(String)

class AuditLog(Record, Base):
    __tablename__ = "audit_logs"
    action: Mapped[str] = mapped_column(String)
    entity_id: Mapped[str] = mapped_column(String)
    data: Mapped[dict] = mapped_column(JSON, default=dict)

class Setting(Base):
    __tablename__ = "settings"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[dict] = mapped_column(JSON)

class WritingTemplate(Record, Base):
    __tablename__ = 'writing_templates'
    template_key: Mapped[str] = mapped_column(String, unique=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String, default='ACTIVE')
    data: Mapped[dict] = mapped_column(JSON)

class StyleUsage(Record, Base):
    __tablename__ = 'style_usage'
    article_id: Mapped[str] = mapped_column(String)
    article_version: Mapped[int] = mapped_column(Integer)
    template_key: Mapped[str] = mapped_column(String)
    template_version: Mapped[int] = mapped_column(Integer)
    tones: Mapped[list] = mapped_column(JSON)

class WritingHarness(Record, Base):
    __tablename__ = 'writing_harness'
    harness_key: Mapped[str] = mapped_column(String, unique=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    data: Mapped[dict] = mapped_column(JSON)
