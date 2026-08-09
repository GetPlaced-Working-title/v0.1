"""Qdrant vector database client."""

from __future__ import annotations

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import get_settings

settings = get_settings()

_qdrant_client: QdrantClient | None = None


def get_qdrant() -> QdrantClient:
    """Get or create the Qdrant client singleton."""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key or None,
            timeout=30,
        )
    return _qdrant_client


def close_qdrant() -> None:
    """Close the Qdrant client."""
    global _qdrant_client
    if _qdrant_client is not None:
        _qdrant_client.close()
        _qdrant_client = None


class QdrantService:
    """High-level Qdrant operations for candidate and job embeddings."""

    def __init__(self, client: QdrantClient | None = None) -> None:
        self._client = client or get_qdrant()

    def ensure_collection(self, collection_name: str, vector_size: int | None = None) -> None:
        """Create collection if it doesn't exist."""
        size = vector_size or settings.qdrant_vector_size
        collections = [c.name for c in self._client.get_collections().collections]
        if collection_name not in collections:
            self._client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=size,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_vector(
        self,
        collection_name: str,
        point_id: str,
        vector: list[float],
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Insert or update a single vector."""
        self._client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload or {},
                )
            ],
        )

    def upsert_vectors(
        self,
        collection_name: str,
        points: list[dict[str, Any]],
    ) -> None:
        """Batch insert/update vectors."""
        structs = [
            PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p.get("payload", {}),
            )
            for p in points
        ]
        self._client.upsert(
            collection_name=collection_name,
            points=structs,
        )

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 50,
        score_threshold: float | None = None,
        filter_conditions: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search for similar vectors."""
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        query_filter = None
        if filter_conditions:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filter_conditions.items()
            ]
            query_filter = Filter(must=conditions)

        results = self._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
        )
        return [
            {
                "id": str(r.id),
                "score": r.score,
                "payload": r.payload,
            }
            for r in results
        ]

    def delete_vector(self, collection_name: str, point_id: str) -> None:
        """Delete a single vector."""
        from qdrant_client.models import PointIdsList

        self._client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(points=[point_id]),
        )

    def get_vector(self, collection_name: str, point_id: str) -> dict[str, Any] | None:
        """Retrieve a single vector by ID."""
        results = self._client.retrieve(
            collection_name=collection_name,
            ids=[point_id],
        )
        if results:
            point = results[0]
            return {
                "id": str(point.id),
                "vector": point.vector,
                "payload": point.payload,
            }
        return None
