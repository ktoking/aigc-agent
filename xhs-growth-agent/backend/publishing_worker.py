"""常驻单进程串行队列，不依赖内容调度或交互式 Codex。"""
import asyncio
from sqlalchemy import select
from .db import SessionLocal
from .models import PublishJob
from .service import PublishingAgent, settings, save_settings, start_run, finish_run

class PublishingWorker:
    def __init__(self, session_factory=SessionLocal, publisher_factory=PublishingAgent, interval=5.0):
        self.session_factory = session_factory
        self.publisher_factory = publisher_factory
        self.interval = interval
        self.task = None
        self.stopping = False
        self.wake = asyncio.Event()
        self.last_error = None

    async def tick(self):
        with self.session_factory() as session:
            if settings(session)["paused"]:
                return "PAUSED"
            uncertain = session.scalar(select(PublishJob).where(PublishJob.mode == "live", PublishJob.status == "VERIFY_REQUIRED"))
            if uncertain:
                save_settings(session, {"paused": True})
                return "VERIFY_REQUIRED"
            inflight = session.scalar(select(PublishJob).where(PublishJob.mode == "live", PublishJob.status == "PUBLISHING"))
            if inflight:
                if not PublishingAgent._lock.locked():
                    from .service import recover
                    recover(session)
                    return "VERIFY_REQUIRED"
                return "IN_PROGRESS"
            job = session.scalar(select(PublishJob).where(PublishJob.status == "QUEUED").order_by(PublishJob.created_at, PublishJob.id))
            if not job:
                return "IDLE"
            # Do not create runs or repeatedly persist quota messages while waiting for the next day.
            if job.mode == "live":
                from datetime import datetime
                from zoneinfo import ZoneInfo
                from sqlalchemy import func
                from .models import PublishAttempt
                today = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
                used = session.scalar(select(func.count()).select_from(PublishAttempt).join(PublishJob, PublishJob.id == PublishAttempt.job_id).where(PublishJob.mode == "live", PublishAttempt.created_at >= today, PublishAttempt.status != "NO_SUBMISSION"))
                if used >= settings(session)["daily_limit"]:
                    if job.error != "今日真实提交配额已用完；队列等待下一日配额":
                        job.error = "今日真实提交配额已用完；队列等待下一日配额"
                        session.commit()
                    return "QUOTA_WAIT"
            run = start_run(session, "Publishing", job.mode)
            await self.publisher_factory().execute(session, job)
            if job.mode == "live" and job.status in {"BLOCKED", "VERIFY_REQUIRED", "FAILED"}:
                save_settings(session, {"paused": True})
            finish_run(session, run, {"job_id": job.id, "article_id": job.article_id, "status": job.status}, "BLOCKED" if job.status in {"BLOCKED", "VERIFY_REQUIRED", "FAILED"} else "COMPLETED")
            return job.status

    async def loop(self):
        while not self.stopping:
            try:
                status = await self.tick()
                self.last_error = None
            except asyncio.CancelledError:
                raise
            except Exception as error:
                self.last_error = type(error).__name__
                status = "ERROR"
            if status in {"PUBLISHED", "MOCK_PUBLISHED", "CANCELLED"}:
                continue  # drain already authorized jobs serially
            self.wake.clear()
            try:
                await asyncio.wait_for(self.wake.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                pass

    def start(self):
        if self.task and not self.task.done():
            return self.task
        self.stopping = False
        self.task = asyncio.create_task(self.loop(), name="xhs-publishing-queue")
        return self.task

    async def stop(self):
        self.stopping = True
        self.wake.set()
        if self.task:
            try:
                await asyncio.wait_for(self.task, timeout=5)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                # Cancellation during a platform write is persisted as VERIFY_REQUIRED by PublishingAgent.
                pass
        self.task = None

worker = PublishingWorker()

def start_publishing_worker():
    return worker.start()

async def stop_publishing_worker():
    await worker.stop()

def wake_publishing_worker():
    worker.wake.set()
