"""Celery tasks for batch matching."""

from __future__ import annotations

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.matching.batch_match_job")
def batch_match_job(job_id: str, top_k: int = 10) -> dict:
    """Run matching pipeline for a job against all candidates."""
    import asyncio
    return asyncio.run(_batch_match_async(job_id, top_k))


async def _batch_match_async(job_id: str, top_k: int) -> dict:
    from app.core.database import async_session_factory
    from app.services.matching import MatchingService

    async with async_session_factory() as session:
        try:
            service = MatchingService(session)
            result = await service.match_candidates(job_id, top_k=top_k)
            await session.commit()

            return {
                "status": "completed",
                "job_id": job_id,
                "matches_found": len(result.get("matches", [])),
                "candidates_evaluated": result.get("total_candidates_evaluated", 0),
            }

        except Exception as e:
            logger.error("batch_match_failed", job_id=job_id, error=str(e))
            return {"status": "failed", "error": str(e)}
