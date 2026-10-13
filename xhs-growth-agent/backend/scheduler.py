import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .db import SessionLocal
from .models import Article, GrowthExperiment
from sqlalchemy import select
from .service import TopicResearchAgent, ChiefEditorAgent, ContentWriterAgent, PublishingAgent, AnalyticsGrowthAgent, quality_review, start_run, finish_run, settings, WorkflowError

TASKS = {"morning_research": (8, 0), "editorial_planning": (8, 30), "content_generation": (9, 0), "quality_review": (10, 0), "publish_approved": (11, 0), "metrics_collection": (20, 0), "daily_review": (21, 0)}
ALIASES = {"research": "morning_research", "plan": "editorial_planning", "generate": "content_generation", "quality": "quality_review", "queue": "publish_approved", "metrics": "metrics_collection", "report": "daily_review"}
LOCKS = {key: asyncio.Lock() for key in TASKS}
scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")

async def execute_task(task):
    task = ALIASES.get(task, task)
    if task not in TASKS:
        raise WorkflowError("未知调度任务")
    lock = LOCKS[task]
    if lock.locked():
        return {"status": "ALREADY_RUNNING", "task": task}
    async with lock:
        with SessionLocal() as session:
            config = settings(session)
            mode = config["model_mode"]
            if task == "morning_research":
                return await TopicResearchAgent().run(session, mode, 100)
            if task == "editorial_planning":
                if mode == "live":
                    return await ChiefEditorAgent().run_live(session, config["production_target"])
                return ChiefEditorAgent().run(session, config["production_target"])
            if task == "content_generation":
                return await ContentWriterAgent().run(session, config["production_target"], mode)
            if task == "publish_approved":
                return await PublishingAgent().run(session)  # existing per-article authorizations only
            if task == "metrics_collection":
                return await AnalyticsGrowthAgent().collect(session)
            if task == "quality_review":
                run = start_run(session, "Quality Reviewer", mode)
                articles = session.scalars(select(Article).where(Article.status.in_(["GENERATED", "PENDING_REVIEW", "QUALITY_REJECTED"]))).all()
                for article in articles:
                    quality_review(session, article)
                result = {"count": len(articles)}
                finish_run(session, run, result)
                return result
            run = start_run(session, "Analytics & Growth", "live")
            result = AnalyticsGrowthAgent().report(session)
            finish_run(session, run, {"date": result["date"], "published": result["published"]})
            return result

def configure_scheduler(enabled):
    if not scheduler.running:
        scheduler.start(paused=True)
    if enabled:
        for task, (hour, minute) in TASKS.items():
            scheduler.add_job(execute_task, "cron", args=[task], id=task, hour=hour, minute=minute, replace_existing=True, max_instances=1, coalesce=True, misfire_grace_time=300)
        scheduler.resume()
    else:
        scheduler.pause()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
