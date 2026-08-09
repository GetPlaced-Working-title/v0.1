"""Portfolio service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.portfolio import Portfolio
from app.repositories.portfolio import PortfolioRepository


class PortfolioService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = PortfolioRepository(session)

    async def add_portfolio(self, candidate_id: str, **kwargs) -> Portfolio:
        return await self.repo.create(
            candidate_id=candidate_id,
            processing_status="pending",
            **kwargs,
        )

    async def get_portfolio(self, portfolio_id: str) -> Portfolio:
        portfolio = await self.repo.get_by_id(portfolio_id)
        if not portfolio:
            raise NotFoundError("Portfolio not found")
        return portfolio

    async def list_portfolios(self, candidate_id: str) -> list[Portfolio]:
        return await self.repo.get_by_candidate(candidate_id)

    async def update_analysis(self, portfolio_id: str, **kwargs) -> Portfolio:
        portfolio = await self.get_portfolio(portfolio_id)
        for key, value in kwargs.items():
            setattr(portfolio, key, value)
        return portfolio
