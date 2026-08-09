"""Base analyzer with caching support."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.client import GeminiClient, get_gemini_client
from app.core.logging import get_logger
from app.models.ai_score import AIAnalysisCache

logger = get_logger(__name__)

# Never call AI twice for the same input — always cache
CACHE_TTL_SECONDS = 30 * 24 * 3600  # 30 days


class BaseAnalyzer(ABC):
    """Base class for all AI analyzers with automatic caching."""

    analyzer_type: str = "base"

    def __init__(self, client: GeminiClient | None = None) -> None:
        self.client = client or get_gemini_client()

    @abstractmethod
    async def analyze(self, content: str, session: AsyncSession | None = None) -> dict[str, Any]:
        """Run the analysis. Must be implemented by subclasses."""
        raise NotImplementedError

    async def _run_with_cache(
        self,
        content: str,
        session: AsyncSession | None,
        prompt_template: str,
    ) -> dict[str, Any]:
        """Run analysis with cache check/write."""
        input_hash = self.client.compute_input_hash(content, self.analyzer_type)

        # Check cache
        if session is not None:
            cached = await self._get_cached(session, input_hash)
            if cached is not None:
                logger.info(
                    "ai_cache_hit",
                    analyzer=self.analyzer_type,
                    input_hash=input_hash[:12],
                )
                return cached

        # Run analysis
        result = await self.client.analyze_text(
            prompt=prompt_template,
            content=content,
        )

        # Write to cache
        if session is not None:
            await self._store_cache(session, input_hash, result)

        return result

    async def _get_cached(
        self,
        session: AsyncSession,
        input_hash: str,
    ) -> dict[str, Any] | None:
        """Retrieve cached analysis result."""
        stmt = select(AIAnalysisCache).where(AIAnalysisCache.input_hash == input_hash)
        result = await session.execute(stmt)
        cached = result.scalar_one_or_none()
        if cached is None:
            return None
        return cached.result

    async def _store_cache(
        self,
        session: AsyncSession,
        input_hash: str,
        result: dict[str, Any],
    ) -> None:
        """Store analysis result in cache."""
        cache_entry = AIAnalysisCache(
            input_hash=input_hash,
            analyzer_type=self.analyzer_type,
            model_used=None,
            result=result,
        )
        session.add(cache_entry)

    async def _store_metadata(
        self,
        session: AsyncSession,
        input_hash: str,
        result: dict[str, Any],
    ) -> None:
        """Store result metadata (tokens, cost) if available."""
        stmt = select(AIAnalysisCache).where(AIAnalysisCache.input_hash == input_hash)
        result_obj = await session.execute(stmt)
        entry = result_obj.scalar_one_or_none()
        if entry is not None:
            if "usage" in result:
                usage = result["usage"]
                entry.input_tokens = usage.get("prompt_tokens")
                entry.output_tokens = usage.get("completion_tokens")
                entry.model_used = usage.get("model")
            # Populate usage into result if present
            result.pop("usage", None)
