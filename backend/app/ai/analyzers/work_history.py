"""Work history analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.work_history import WORK_HISTORY_ANALYSIS_PROMPT


class WorkHistoryAnalyzer(BaseAnalyzer):
    """Analyzes work history for progression and trajectory."""

    analyzer_type = "work_history_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze work history entries."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=WORK_HISTORY_ANALYSIS_PROMPT,
        )