"""Portfolio analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.portfolio import PORTFOLIO_ANALYSIS_PROMPT


class PortfolioAnalyzer(BaseAnalyzer):
    """Analyzes portfolio website content."""

    analyzer_type = "portfolio_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze portfolio content (text extracted from the site)."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=PORTFOLIO_ANALYSIS_PROMPT,
        )
