"""Search router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.schemas.search import CandidateSearchRequest, JobSearchRequest
from app.services.search import SearchService

router = APIRouter(tags=["search"])


@router.post("/candidates")
async def search_candidates(
    data: CandidateSearchRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Keyword search for candidates via Meilisearch."""
    search = SearchService()
    filter_parts = []
    if data.location:
        filter_parts.append(f"location = '{data.location}'")
    if data.open_to_remote is not None:
        filter_parts.append(f"open_to_remote = {str(data.open_to_remote).lower()}")
    if data.evidence_confidence:
        filter_parts.append(f"evidence_confidence = '{data.evidence_confidence}'")

    filter_str = " AND ".join(filter_parts) if filter_parts else None

    results = search.search_candidates(
        query=data.query,
        limit=data.size,
        offset=(data.page - 1) * data.size,
        filter_str=filter_str,
    )
    return results


@router.post("/jobs")
async def search_jobs(
    data: JobSearchRequest,
    current_user: dict = Depends(get_current_user),
):
    """Keyword search for jobs via Meilisearch."""
    search = SearchService()
    filter_parts = ["status = active"]
    if data.location:
        filter_parts.append(f"location = '{data.location}'")
    if data.employment_type:
        filter_parts.append(f"employment_type = '{data.employment_type}'")
    if data.work_mode:
        filter_parts.append(f"work_mode = '{data.work_mode}'")

    filter_str = " AND ".join(filter_parts) if filter_parts else None

    results = search.search_jobs(
        query=data.query,
        limit=data.size,
        offset=(data.page - 1) * data.size,
        filter_str=filter_str,
    )
    return results
