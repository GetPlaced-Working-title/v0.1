"""Authentication router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter(tags=["auth"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user info."""
    service = UserService(db)
    clerk_id = current_user.get("clerk_id")
    user = await service.get_by_clerk_id(clerk_id)
    if not user:
        user = await service.get_or_create_from_clerk(current_user)
    return user
