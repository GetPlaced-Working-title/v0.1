"""Portfolios router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_candidate, get_current_user, get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.services.portfolio import PortfolioService

router = APIRouter(tags=["portfolios"])


@router.post("", response_model=PortfolioResponse)
async def add_portfolio(
    candidate_id: str,
    data: PortfolioCreate,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Add a portfolio URL for analysis."""
    service = PortfolioService(db)
    return await service.add_portfolio(candidate_id, **data.model_dump())


@router.get("", response_model=list[PortfolioResponse])
async def list_portfolios(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List portfolios for a candidate."""
    service = PortfolioService(db)
    return await service.list_portfolios(candidate_id)


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get portfolio by ID."""
    service = PortfolioService(db)
    return await service.get_portfolio(portfolio_id)
