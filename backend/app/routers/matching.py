"""Matching router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    PaginationParams,
    get_current_recruiter,
    get_current_user,
    get_db,
)
from app.schemas.common import paginate
from app.schemas.matching import JobMatchResponse, MatchStatusUpdate
from app.schemas.search import MatchRequest, MatchResponse
from app.services.matching import MatchingService

router = APIRouter(tags=["matching"])


@router.post("/run", response_model=dict)
async def run_matching(
    data: MatchRequest,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Run the full matching pipeline for a job."""
    service = MatchingService(db)
    result = await service.match_candidates(data.job_id, top_k=data.top_k)
    return {
        "job_id": result["job_id"],
        "total_candidates_evaluated": result["total_candidates_evaluated"],
        "matches_count": len(result["matches"]),
    }


@router.get("/jobs/{job_id}", response_model=dict)
async def get_job_matches(
    job_id: str,
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get matches for a job."""
    service = MatchingService(db)
    items, total = await service.get_job_matches(
        job_id, offset=pagination.offset, limit=pagination.size
    )
    return paginate(items, total, pagination.page, pagination.size)


@router.patch("/matches/{match_id}", response_model=JobMatchResponse)
async def update_match_status(
    match_id: str,
    data: MatchStatusUpdate,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Update match status (shortlist, reject, etc)."""
    service = MatchingService(db)
    return await service.update_match_status(match_id, data.status, data.recruiter_notes)
