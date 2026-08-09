"""Resume analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.resume import RESUME_ANALYSIS_PROMPT


class ResumeAnalyzer(BaseAnalyzer):
    """Analyzes resume text and produces structured profile + scores."""

    analyzer_type = "resume_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze a resume's raw text."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=RESUME_ANALYSIS_PROMPT,
        )
