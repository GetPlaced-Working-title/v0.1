"""Companies router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_recruiter, get_current_user, get_db
from app.schemas.common import paginate
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company import CompanyService

router = APIRouter(tags=["companies"])


@router.post("", response_model=CompanyResponse)
async def create_company(
    data: CompanyCreate,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Create a company profile (recruiter only)."""
    service = CompanyService(db)
    user_id = current_user.get("user_id", "")
    return await service.create_company(user_id=user_id, **data.model_dump())


@router.get("", response_model=dict)
async def list_companies(
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List companies."""
    service = CompanyService(db)
    items, total = await service.list_companies(
        offset=pagination.offset, limit=pagination.size
    )
    return paginate(items, total, pagination.page, pagination.size)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get company by ID."""
    service = CompanyService(db)
    return await service.get_company(company_id)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    data: CompanyUpdate,
    current_user: dict = Depends(get_current_recruiter),
    db: AsyncSession = Depends(get_db),
):
    """Update company profile."""
    service = CompanyService(db)
    return await service.update_company(company_id, **data.model_dump(exclude_unset=True))
