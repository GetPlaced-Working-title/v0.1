"""Shared schemas for pagination, errors, and standard responses."""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)


class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    error: str
    request_id: str | None = None
    details: Any | None = None


class MessageResponse(BaseModel):
    message: str


class IDResponse(BaseModel):
    id: str


def paginate(items: list[Any], total: int, page: int, size: int) -> dict[str, Any]:
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size if size > 0 else 0,
    }
