"""Recommendation letter analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.recommendation import RECOMMENDATION_ANALYSIS_PROMPT


class RecommendationAnalyzer(BaseAnalyzer):
    """Analyzes recommendation letters for credibility and substance."""

    analyzer_type = "recommendation_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze a recommendation letter's content."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=RECOMMENDATION_ANALYSIS_PROMPT,
        )