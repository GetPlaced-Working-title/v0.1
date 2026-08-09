"""Jobs router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_recruiter, get_current_user, get_db
from app.schemas.common import paginate
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job import JobService

router = APIRouter(tags=["jobs"])


@router.post("", response_model=JobResponse)
async def create_job(
    company_id: str,
    data: JobCreate,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Create a job posting."""
    service = JobService(db)
    return await service.create_job(company_id=company_id, **data.model_dump())


@router.get("", response_model=dict)
async def list_jobs(
    company_id: str | None = None,
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List jobs. Filter by company or list active jobs."""
    service = JobService(db)
    if company_id:
        items, total = await service.list_by_company(
            company_id, offset=pagination.offset, limit=pagination.size
        )
    else:
        items, total = await service.list_active(
            offset=pagination.offset, limit=pagination.size
        )
    return paginate(items, total, pagination.page, pagination.size)


@router.get("/search", response_model=dict)
async def search_jobs(
    query: str = "",
    location: str | None = None,
    employment_type: str | None = None,
    work_mode: str | None = None,
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Search active jobs."""
    service = JobService(db)
    items, total = await service.search_jobs(
        query=query,
        location=location,
        employment_type=employment_type,
        work_mode=work_mode,
        offset=pagination.offset,
        limit=pagination.size,
    )
    return paginate(items, total, pagination.page, pagination.size)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get job by ID."""
    service = JobService(db)
    return await service.get_job(job_id)


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    data: JobUpdate,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Update job posting."""
    service = JobService(db)
    return await service.update_job(job_id, **data.model_dump(exclude_unset=True))


@router.post("/{job_id}/publish", response_model=JobResponse)
async def publish_job(
    job_id: str,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Publish a draft job."""
    service = JobService(db)
    return await service.publish_job(job_id)


@router.post("/{job_id}/close", response_model=JobResponse)
async def close_job(
    job_id: str,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Close a job posting."""
    service = JobService(db)
    return await service.close_job(job_id)
