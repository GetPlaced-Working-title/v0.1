"""Vector search over Qdrant (semantic matching)."""

from __future__ import annotations

from typing import Any

from app.ai.client import get_gemini_client
from app.core.config import get_settings
from app.core.qdrant import QdrantService

settings = get_settings()


class VectorSearchService:
    """Semantic search for top candidates given a job query vector."""

    def __init__(self, qdrant: QdrantService | None = None) -> None:
        self._qdrant = qdrant or QdrantService()
        self._client = get_gemini_client()

    async def search_candidates(
        self,
        job_embedding: list[float],
        limit: int = 50,
        score_threshold: float | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search the candidates collection for the closest matches."""
        collection = settings.qdrant_collection_candidates
        return self._qdrant.search(
            collection_name=collection,
            query_vector=job_embedding,
            limit=limit,
            score_threshold=score_threshold,
            filter_conditions=filters,
        )

    async def search_matches_for_job(
        self,
        job_purpose: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Search candidates given a job description text."""
        query_vector = await self._client.generate_query_embedding(job_purpose)
        return await self.search_candidates(query_vector, limit=limit)
