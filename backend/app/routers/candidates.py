"""Candidates router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    PaginationParams,
    get_current_candidate,
    get_current_user,
    get_db,
)
from app.schemas.candidate import (
    CandidateCreate,
    CandidateListResponse,
    CandidateResponse,
    CandidateUpdate,
)
from app.schemas.common import paginate
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.work_history import WorkHistoryCreate, WorkHistoryResponse
from app.schemas.recommendation import RecommendationCreate, RecommendationResponse
from app.schemas.skill import SkillResponse
from app.services.candidate import CandidateService
from app.repositories.project import ProjectRepository

router = APIRouter(tags=["candidates"])


@router.post("", response_model=CandidateResponse)
async def create_candidate(
    data: CandidateCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a candidate profile."""
    service = CandidateService(db)
    user_id = current_user.get("user_id", "")
    return await service.create_candidate(user_id=user_id, **data.model_dump())


@router.get("", response_model=dict)
async def list_candidates(
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all candidates."""
    service = CandidateService(db)
    items, total = await service.list_candidates(
        offset=pagination.offset, limit=pagination.size
    )
    return paginate(items, total, pagination.page, pagination.size)


@router.get("/search", response_model=dict)
async def search_candidates(
    query: str = "",
    location: str | None = None,
    min_experience: int | None = None,
    open_to_remote: bool | None = None,
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Search candidates."""
    service = CandidateService(db)
    items, total = await service.search_candidates(
        query=query,
        location=location,
        min_experience=min_experience,
        open_to_remote=open_to_remote,
        offset=pagination.offset,
        limit=pagination.size,
    )
    return paginate(items, total, pagination.page, pagination.size)


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get candidate by ID."""
    service = CandidateService(db)
    return await service.get_candidate(candidate_id)


@router.patch("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: str,
    data: CandidateUpdate,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Update candidate profile."""
    service = CandidateService(db)
    return await service.update_candidate(candidate_id, **data.model_dump(exclude_unset=True))


@router.post("/{candidate_id}/projects", response_model=ProjectResponse)
async def add_project(
    candidate_id: str,
    data: ProjectCreate,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Add a project to candidate profile."""
    from app.repositories.project import ProjectRepository
    repo = ProjectRepository(db)
    from app.models.project import Project
    project = await repo.create(candidate_id=candidate_id, **data.model_dump())
    return project


@router.get("/{candidate_id}/projects", response_model=list[ProjectResponse])
async def list_projects(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List candidate projects."""
    from app.repositories.project import ProjectRepository
    repo = ProjectRepository(db)
    return await repo.get_by_candidate(candidate_id)


@router.post("/{candidate_id}/work-history", response_model=WorkHistoryResponse)
async def add_work_history(
    candidate_id: str,
    data: WorkHistoryCreate,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Add work history entry."""
    from app.repositories.base import BaseRepository
    from app.models.work_history import WorkHistory
    repo = BaseRepository(WorkHistory, db)
    return await repo.create(candidate_id=candidate_id, **data.model_dump())


@router.get("/{candidate_id}/work-history", response_model=list[WorkHistoryResponse])
async def list_work_history(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List candidate work history."""
    from app.repositories.base import BaseRepository
    from app.models.work_history import WorkHistory
    repo = BaseRepository(WorkHistory, db)
    items = await repo.get_all(
        filters={"candidate_id": candidate_id},
        order_by=WorkHistory.start_date.desc(),
    )
    return items


@router.post("/{candidate_id}/recommendations", response_model=RecommendationResponse)
async def add_recommendation(
    candidate_id: str,
    data: RecommendationCreate,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Add a recommendation."""
    from app.repositories.base import BaseRepository
    from app.models.recommendation import Recommendation
    repo = BaseRepository(Recommendation, db)
    return await repo.create(candidate_id=candidate_id, source="manual", **data.model_dump())


@router.get("/{candidate_id}/skills", response_model=list[SkillResponse])
async def list_skills(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List candidate skills."""
    from app.repositories.skill import SkillRepository
    repo = SkillRepository(db)
    return await repo.get_by_candidate(candidate_id)
