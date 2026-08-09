"""Search service — hybrid search across candidates and jobs."""

from __future__ import annotations

from typing import Any

from app.core.logging import get_logger
from app.core.meilisearch import MeilisearchService
from app.core.qdrant import QdrantService

logger = get_logger(__name__)


class SearchService:
    """Orchestrates keyword (Meilisearch) and vector (Qdrant) search."""

    def __init__(self) -> None:
        self.meili = MeilisearchService()
        self.qdrant = QdrantService()

    def index_candidate(self, candidate_id: str, data: dict[str, Any]) -> None:
        """Index a candidate in Meilisearch."""
        doc = {"id": candidate_id, **data}
        self.meili.add_documents("candidates", [doc])

    def index_job(self, job_id: str, data: dict[str, Any]) -> None:
        """Index a job in Meilisearch."""
        doc = {"id": job_id, **data}
        self.meili.add_documents("jobs", [doc])

    def search_candidates(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        filter_str: str | None = None,
    ) -> dict[str, Any]:
        """Keyword search for candidates."""
        return self.meili.search(
            "candidates",
            query=query,
            limit=limit,
            offset=offset,
            filter_str=filter_str,
        )

    def search_jobs(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        filter_str: str | None = None,
    ) -> dict[str, Any]:
        """Keyword search for jobs."""
        return self.meili.search(
            "jobs",
            query=query,
            limit=limit,
            offset=offset,
            filter_str=filter_str,
        )

    def remove_candidate(self, candidate_id: str) -> None:
        try:
            self.meili.delete_document("candidates", candidate_id)
        except Exception:
            logger.warning("meili_delete_failed", candidate_id=candidate_id)

    def remove_job(self, job_id: str) -> None:
        try:
            self.meili.delete_document("jobs", job_id)
        except Exception:
            logger.warning("meili_delete_failed", job_id=job_id)
