"""Certificate analyzer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.certificate import CERTIFICATE_ANALYSIS_PROMPT


class CertificateAnalyzer(BaseAnalyzer):
    """Analyzes certifications for credibility and relevance."""

    analyzer_type = "certificate_analysis"

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """Analyze certificate details."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=CERTIFICATE_ANALYSIS_PROMPT,
        )