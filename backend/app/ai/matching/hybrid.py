"""Hybrid search — merges keyword and vector results.

Uses Reciprocal Rank Fusion (RRF) to combine Meilisearch keyword results
with Qdrant semantic results. Smaller embedding models work well here
because keyword search handles exact matches — hybrid gives better recall
than semantic-only.
"""

from __future__ import annotations

from typing import Any

from app.ai.matching.keyword_search import KeywordSearchService
from app.ai.matching.vector_search import VectorSearchService
from app.core.logging import get_logger

logger = get_logger(__name__)

RRF_K = 60  # Reciprocal Rank Fusion constant


class HybridSearchService:
    """Combines keyword and vector search signals."""

    KEYWORD_WEIGHT = 0.4
    VECTOR_WEIGHT = 0.6

    def __init__(
        self,
        keyword_service: KeywordSearchService | None = None,
        vector_service: VectorSearchService | None = None,
    ) -> None:
        self._keyword = keyword_service or KeywordSearchService()
        self._vector = vector_service or VectorSearchService()

    async def search(
        self,
        query: str,
        limit: int = 50,
        filters_keyword: dict[str, Any] | None = None,
        filters_vector: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Run hybrid search and return merged, ranked results."""
        vector_results = await self._vector.search_matches_for_job(query, limit=limit * 2)
        keyword_results = self._keyword.search(
            query, limit=limit * 2, offset=0, filters=filters_keyword
        )
        return self._merge(keyword_results, vector_results, limit)

    def _merge(
        self,
        keyword_results: list[dict[str, Any]],
        vector_results: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        """Merge with weighted reciprocal rank fusion."""
        merged: dict[str, dict[str, Any]] = {}

        def _key(hit: dict[str, Any], is_vector: bool) -> str | None:
            if is_vector:
                payload = hit.get("payload") or {}
                return str(payload.get("candidate_id")) or str(hit.get("id"))
            return str(hit.get("id"))

        for rank, hit in enumerate(keyword_results):
            candidate_id = _key(hit, is_vector=False)
            if not candidate_id:
                continue
            rrf = 1.0 / (RRF_K + rank + 1)
            item = merged.setdefault(
                candidate_id,
                {
                    "candidate_id": candidate_id,
                    "keyword_score": 0.0,
                    "vector_score": 0.0,
                    "_rrf": 0.0,
                },
            )
            item["keyword_score"] = self._normalize(1.0 - (rank / max(1, len(keyword_results))))
            item["_rrf"] += self.KEYWORD_WEIGHT * rrf

        for rank, hit in enumerate(vector_results):
            candidate_id = _key(hit, is_vector=True)
            if not candidate_id:
                continue
            rrf = 1.0 / (RRF_K + rank + 1)
            item = merged.setdefault(
                candidate_id,
                {
                    "candidate_id": candidate_id,
                    "keyword_score": 0.0,
                    "vector_score": 0.0,
                    "_rrf": 0.0,
                },
            )
            item["vector_score"] = max(item["vector_score"], float(hit.get("score", 0.0)))
            item["_rrf"] += self.VECTOR_WEIGHT * rrf

        results = list(merged.values())
        for item in results:
            item["hybrid_score"] = round(min(1.0, item["_rrf"] * 5), 4)
        results.sort(key=lambda x: x["hybrid_score"], reverse=True)

        return [
            {
                "candidate_id": item["candidate_id"],
                "keyword_score": round(item["keyword_score"], 4),
                "vector_score": round(item["vector_score"], 4),
                "hybrid_score": item["hybrid_score"],
            }
            for item in results[:limit]
        ]

    @staticmethod
    def _normalize(score: float) -> float:
        """Clamp a normalized score between 0 and 1."""
        return round(max(0.0, min(1.0, float(score))), 4)
