"""Resume repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Resume, session)

    async def get_by_candidate(self, candidate_id: str) -> list[Resume]:
        stmt = (
            select(Resume)
            .where(Resume.candidate_id == candidate_id)
            .order_by(Resume.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_primary(self, candidate_id: str) -> Resume | None:
        stmt = select(Resume).where(
            Resume.candidate_id == candidate_id,
            Resume.is_primary == True,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
