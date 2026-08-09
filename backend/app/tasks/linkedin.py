"""Celery tasks for LinkedIn analysis."""

from __future__ import annotations

from datetime import UTC

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.linkedin.analyze_linkedin")
def analyze_linkedin(linkedin_id: str) -> dict:
    """Analyze LinkedIn export data."""
    import asyncio
    return asyncio.run(_analyze_linkedin_async(linkedin_id))


async def _analyze_linkedin_async(linkedin_id: str) -> dict:
    from app.ai.analyzers.linkedin import LinkedInAnalyzer
    from app.core.database import async_session_factory
    from app.models.linkedin import LinkedInExport
    from app.repositories.base import BaseRepository

    async with async_session_factory() as session:
        repo = BaseRepository(LinkedInExport, session)
        linkedin = await repo.get_by_id(linkedin_id)
        if not linkedin:
            return {"error": "LinkedIn export not found"}

        try:
            linkedin.processing_status = "processing"
            await session.commit()

            analyzer = LinkedInAnalyzer()
            content = linkedin.about or ""
            if linkedin.experience:
                import json
                content += f"\nExperience: {json.dumps(linkedin.experience)}"
            if linkedin.skills:
                import json
                content += f"\nSkills: {json.dumps(linkedin.skills)}"

            analysis = await analyzer.analyze(content, session)

            linkedin.analysis = analysis
            linkedin.scores = analysis.get("scores", {})

            from datetime import datetime
            linkedin.analyzed_at = datetime.now(UTC)
            linkedin.processing_status = "completed"
            await session.commit()

            return {"status": "completed", "linkedin_id": linkedin_id}

        except Exception as e:
            linkedin.processing_status = "failed"
            linkedin.processing_error = str(e)
            await session.commit()
            return {"status": "failed", "error": str(e)}
