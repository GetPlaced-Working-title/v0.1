"""GitHub router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_candidate, get_current_user, get_db
from app.schemas.github import GitHubConnect, GitHubProfileResponse
from app.services.github import GitHubService

router = APIRouter(tags=["github"])


@router.post("/connect", response_model=GitHubProfileResponse)
async def connect_github(
    candidate_id: str,
    data: GitHubConnect,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Connect a GitHub account for analysis."""
    service = GitHubService(db)
    return await service.connect_github(candidate_id, data.username)


@router.get("", response_model=GitHubProfileResponse)
async def get_github_profile(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get GitHub profile for a candidate."""
    service = GitHubService(db)
    return await service.get_profile(candidate_id)
