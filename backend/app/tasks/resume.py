"""Celery tasks for resume processing."""

from __future__ import annotations

from datetime import UTC

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.resume.process_resume")
def process_resume(resume_id: str) -> dict:
    """Process a resume: extract text, run AI analysis, store results."""
    import asyncio
    return asyncio.run(_process_resume_async(resume_id))


async def _process_resume_async(resume_id: str) -> dict:
    from app.ai.analyzers.resume import ResumeAnalyzer
    from app.core.database import async_session_factory
    from app.models.resume import Resume
    from app.repositories.base import BaseRepository

    async with async_session_factory() as session:
        repo = BaseRepository(Resume, session)
        resume = await repo.get_by_id(resume_id)
        if not resume:
            return {"error": "Resume not found"}

        try:
            resume.processing_status = "processing"
            await session.commit()

            analyzer = ResumeAnalyzer()
            raw_text = resume.raw_text or ""
            if not raw_text and resume.file_url:
                raw_text = f"Resume file at: {resume.file_url}"

            analysis = await analyzer.analyze(raw_text, session)

            resume.analysis = analysis
            resume.scores = analysis.get("scores", {})
            resume.basic_info = analysis.get("basic_info", {})
            resume.experience = analysis.get("experience", {})
            resume.education = analysis.get("education", {})
            resume.skills_extracted = analysis.get("skills", {})
            resume.processing_status = "completed"

            from datetime import datetime
            resume.analyzed_at = datetime.now(UTC)
            await session.commit()

            return {"status": "completed", "resume_id": resume_id}

        except Exception as e:
            resume.processing_status = "failed"
            resume.processing_error = str(e)
            await session.commit()
            logger.error("resume_processing_failed", resume_id=resume_id, error=str(e))
            return {"status": "failed", "error": str(e)}
