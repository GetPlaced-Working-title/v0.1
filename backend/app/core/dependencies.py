"""FastAPI dependency injection."""

from __future__ import annotations

from typing import Any

from fastapi import Depends, Query

from app.core.database import get_db as _get_db
from app.core.security import get_current_user, role_required


async def get_db() -> Any:
    """Re-export database session dependency."""
    async for session in _get_db():
        yield session


async def get_current_candidate(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Require the current user to be a candidate."""
    checker = role_required("candidate", "admin")
    return await checker(current_user)


async def get_current_recruiter(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Require the current user to be a recruiter."""
    checker = role_required("recruiter", "admin")
    return await checker(current_user)


async def get_current_admin(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Require the current user to be an admin."""
    checker = role_required("admin")
    return await checker(current_user)


class PaginationParams:
    """Pagination parameters."""

    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(20, ge=1, le=100, description="Items per page"),
    ) -> None:
        self.page = page
        self.size = size
        self.offset = (page - 1) * size
