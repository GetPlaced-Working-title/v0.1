"""Celery tasks for video analysis."""

from __future__ import annotations

from datetime import UTC

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.video.analyze_video")
def analyze_video(video_id: str) -> dict:
    """Analyze a skill demonstration video."""
    import asyncio
    return asyncio.run(_analyze_video_async(video_id))


async def _analyze_video_async(video_id: str) -> dict:
    from app.ai.analyzers.video import VideoAnalyzer
    from app.core.database import async_session_factory
    from app.models.video import Video
    from app.repositories.base import BaseRepository

    async with async_session_factory() as session:
        repo = BaseRepository(Video, session)
        video = await repo.get_by_id(video_id)
        if not video:
            return {"error": "Video not found"}

        try:
            video.processing_status = "processing"
            await session.commit()

            analyzer = VideoAnalyzer()
            analysis = await analyzer.analyze(video.file_url, session)

            video.analysis = analysis
            video.scores = analysis.get("scores", {})
            video.transcript = analysis.get("transcript")

            from datetime import datetime
            video.analyzed_at = datetime.now(UTC)
            video.processing_status = "completed"
            await session.commit()

            return {"status": "completed", "video_id": video_id}

        except Exception as e:
            video.processing_status = "failed"
            video.processing_error = str(e)
            await session.commit()
            return {"status": "failed", "error": str(e)}
