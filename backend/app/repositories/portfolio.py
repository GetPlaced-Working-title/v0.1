"""Portfolio repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portfolio import Portfolio
from app.repositories.base import BaseRepository


class PortfolioRepository(BaseRepository[Portfolio]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Portfolio, session)

    async def get_by_candidate(self, candidate_id: str) -> list[Portfolio]:
        stmt = (
            select(Portfolio)
            .where(Portfolio.candidate_id == candidate_id)
            .order_by(Portfolio.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
