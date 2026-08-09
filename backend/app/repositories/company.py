"""Company repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Company, session)

    async def get_by_user_id(self, user_id: str) -> Company | None:
        stmt = select(Company).where(Company.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
