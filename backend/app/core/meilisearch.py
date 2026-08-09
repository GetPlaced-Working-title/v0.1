"""Meilisearch client for keyword search."""

from __future__ import annotations

from typing import Any

import meilisearch

from app.core.config import get_settings

settings = get_settings()

_meili_client: meilisearch.Client | None = None


def get_meilisearch() -> meilisearch.Client:
    """Get or create the Meilisearch client singleton."""
    global _meili_client
    if _meili_client is None:
        _meili_client = meilisearch.Client(
            settings.meilisearch_url,
            settings.meilisearch_api_key,
        )
    return _meili_client


class MeilisearchService:
    """High-level Meilisearch operations."""

    def __init__(self, client: meilisearch.Client | None = None) -> None:
        self._client = client or get_meilisearch()

    def ensure_index(
        self,
        index_name: str,
        primary_key: str = "id",
        searchable_attributes: list[str] | None = None,
        filterable_attributes: list[str] | None = None,
        sortable_attributes: list[str] | None = None,
    ) -> None:
        """Create index and configure attributes."""
        try:
            self._client.get_index(index_name)
        except Exception:
            self._client.create_index(index_name, {"primaryKey": primary_key})

        index = self._client.index(index_name)
        if searchable_attributes:
            index.update_searchable_attributes(searchable_attributes)
        if filterable_attributes:
            index.update_filterable_attributes(filterable_attributes)
        if sortable_attributes:
            index.update_sortable_attributes(sortable_attributes)

    def add_documents(
        self,
        index_name: str,
        documents: list[dict[str, Any]],
        primary_key: str = "id",
    ) -> None:
        """Add or update documents in an index."""
        index = self._client.index(index_name)
        index.add_documents(documents, primary_key=primary_key)

    def search(
        self,
        index_name: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
        filter_str: str | None = None,
        sort: list[str] | None = None,
        attributes_to_retrieve: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search an index."""
        index = self._client.index(index_name)
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }
        if filter_str:
            params["filter"] = filter_str
        if sort:
            params["sort"] = sort
        if attributes_to_retrieve:
            params["attributesToRetrieve"] = attributes_to_retrieve

        return index.search(query, params)

    def delete_document(self, index_name: str, document_id: str) -> None:
        """Delete a document from an index."""
        index = self._client.index(index_name)
        index.delete_document(document_id)

    def update_document(
        self,
        index_name: str,
        document: dict[str, Any],
        primary_key: str = "id",
    ) -> None:
        """Update a single document."""
        index = self._client.index(index_name)
        index.update_documents([document], primary_key=primary_key)

    def delete_index(self, index_name: str) -> None:
        """Delete an entire index."""
        self._client.delete_index(index_name)
