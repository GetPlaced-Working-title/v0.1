"""LinkedIn analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.linkedin import LINKEDIN_ANALYSIS_PROMPT


class LinkedInAnalyzer(BaseAnalyzer):
    """Analyzes LinkedIn profile data (from export or OAuth)."""

    analyzer_type = "linkedin_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze LinkedIn profile content."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=LINKEDIN_ANALYSIS_PROMPT,
        )
