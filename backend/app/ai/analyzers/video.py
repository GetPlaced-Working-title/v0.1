"""Video analyzer using Gemini Video model."""

from __future__ import annotations

import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.video import VIDEO_ANALYSIS_PROMPT
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class VideoAnalyzer(BaseAnalyzer):
    """Analyzes skill demonstration videos for communication and technical depth."""

    analyzer_type = "video_analysis"

    async def upload_video_file(self, file_path: str) -> Any:
        """Upload video to Gemini and wait for processing."""
        video_file = genai.upload_file(file_path)
        logger.info("video_uploaded", uri=video_file.uri)

        # Wait for processing to complete
        import time

        timeout = 120
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            video_file = genai.get_file(video_file.name)
            if video_file.state.name == "ACTIVE":
                break
            await self._sleep(5)

        if video_file.state.name != "ACTIVE":
            logger.warning("video_processing_timeout", name=video_file.name)

        return video_file

    async def analyze_video(
        self,
        video_file: Any,
        session: AsyncSession | None = None,
    ) -> dict:
        """Analyze an uploaded video file."""
        result = await self.client.analyze_video(
            prompt=VIDEO_ANALYSIS_PROMPT,
            video_file=video_file,
        )
        return result

    async def analyze_transcript(
        self,
        transcript: str,
        session: AsyncSession | None = None,
    ) -> dict:
        """Analyze a video transcript without the video file."""
        return await self._run_with_cache(
            content=transcript,
            session=session,
            prompt_template=VIDEO_ANALYSIS_PROMPT,
        )

    @staticmethod
    async def _sleep(seconds: float) -> None:
        import asyncio

        await asyncio.sleep(seconds)
