"""Admin router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin, get_db
from app.repositories.candidate import CandidateRepository
from app.repositories.job import JobRepository
from app.repositories.job_match import JobMatchRepository
from app.repositories.user import UserRepository

router = APIRouter(tags=["admin"])


@router.get("/stats")
async def get_platform_stats(
    current_user: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get platform-wide statistics."""
    user_repo = UserRepository(db)
    candidate_repo = CandidateRepository(db)
    job_repo = JobRepository(db)
    match_repo = JobMatchRepository(db)

    total_users = await user_repo.count()
    total_candidates = await candidate_repo.count()
    total_jobs = await job_repo.count()
    total_matches = await match_repo.count()
    active_jobs = await job_repo.count(filters={"status": "active"})

    return {
        "total_users": total_users,
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_matches": total_matches,
    }


@router.get("/users")
async def list_users(
    current_user: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin only)."""
    repo = UserRepository(db)
    users = await repo.get_all(limit=100)
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
        }
        for u in users
    ]
