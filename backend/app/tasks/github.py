"""Celery tasks for GitHub analysis."""

from __future__ import annotations

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.github.analyze_github")
def analyze_github(profile_id: str) -> dict:
    """Fetch GitHub data and run AI analysis."""
    import asyncio
    return asyncio.run(_analyze_github_async(profile_id))


async def _analyze_github_async(profile_id: str) -> dict:
    from app.core.database import async_session_factory
    from app.ai.analyzers.github import GitHubAnalyzer
    from app.repositories.base import BaseRepository
    from app.models.github_profile import GitHubProfile

    async with async_session_factory() as session:
        repo = BaseRepository(GitHubProfile, session)
        profile = await repo.get_by_id(profile_id)
        if not profile:
            return {"error": "GitHub profile not found"}

        try:
            profile.processing_status = "processing"
            await session.commit()

            analyzer = GitHubAnalyzer()
            analysis = await analyzer.fetch_and_analyze(
                profile.username, session
            )

            profile.analysis = analysis
            profile.scores = analysis.get("scores", {})
            profile.profile_data = analysis.get("profile_data", {})
            profile.repositories = analysis.get("repository_data", [])
            profile.primary_languages = analysis.get("primary_languages", {})

            from datetime import datetime, timezone
            profile.analyzed_at = datetime.now(timezone.utc)
            profile.last_fetched_at = datetime.now(timezone.utc)
            profile.processing_status = "completed"
            await session.commit()

            return {"status": "completed", "profile_id": profile_id}

        except Exception as e:
            profile.processing_status = "failed"
            profile.processing_error = str(e)
            await session.commit()
            logger.error("github_analysis_failed", profile_id=profile_id, error=str(e))
            return {"status": "failed", "error": str(e)}
