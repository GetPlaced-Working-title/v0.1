"""Project analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.project import PROJECT_ANALYSIS_PROMPT


class ProjectAnalyzer(BaseAnalyzer):
    """Analyzes a project description for quality and depth."""

    analyzer_type = "project_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze a single project description."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=PROJECT_ANALYSIS_PROMPT,
        )
