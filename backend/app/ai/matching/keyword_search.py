"""Keyword search over Meilisearch."""

from __future__ import annotations

from typing import Any

from app.core.meilisearch import MeilisearchService


class KeywordSearchService:
    """Deterministic keyword search for candidates."""

    INDEX_NAME = "candidates"

    def __init__(self, meili: MeilisearchService | None = None) -> None:
        self._meili = meili or MeilisearchService()

    def search(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search candidates by keywords."""
        filter_str = self._build_filter(filters) if filters else None
        result = self._meili.search(
            self.INDEX_NAME,
            query,
            limit=limit,
            offset=offset,
            filter_str=filter_str,
        )
        return result.get("hits", [])

    def _build_filter(self, filters: dict[str, Any]) -> str:
        """Build a Meilisearch filter string from a dict."""
        parts = []
        for key, value in filters.items():
            if isinstance(value, list):
                parts.append(f"{key} IN [{', '.join(repr(v) for v in value)}]")
            else:
                parts.append(f"{key} = {value!r}")
        return " AND ".join(parts)