"""Candidate repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.base import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Candidate, session)

    async def get_by_user_id(self, user_id: str) -> Candidate | None:
        stmt = select(Candidate).where(Candidate.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def search(
        self,
        query: str | None = None,
        location: str | None = None,
        min_experience: int | None = None,
        skills: list[str] | None = None,
        open_to_remote: bool | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Candidate], int]:
        stmt = select(Candidate)
        count_stmt = select(Candidate)

        if query:
            like = f"%{query}%"
            condition = Candidate.name.ilike(like) | Candidate.headline.ilike(like)
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)
        if location:
            stmt = stmt.where(Candidate.location.ilike(f"%{location}%"))
            count_stmt = count_stmt.where(Candidate.location.ilike(f"%{location}%"))
        if min_experience is not None:
            stmt = stmt.where(Candidate.years_of_experience >= min_experience)
            count_stmt = count_stmt.where(Candidate.years_of_experience >= min_experience)
        if open_to_remote is not None:
            stmt = stmt.where(Candidate.open_to_remote == open_to_remote)
            count_stmt = count_stmt.where(Candidate.open_to_remote == open_to_remote)

        total_result = await self.session.execute(
            select(Candidate.id).select_from(count_stmt.subquery())
        )
        total = len(total_result.all())

        stmt = stmt.order_by(Candidate.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total
