"""Job match repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_match import JobMatch
from app.repositories.base import BaseRepository


class JobMatchRepository(BaseRepository[JobMatch]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(JobMatch, session)

    async def get_by_job(
        self, job_id: str, offset: int = 0, limit: int = 20
    ) -> tuple[list[JobMatch], int]:
        filters = {"job_id": job_id}
        items = await self.get_all(
            offset=offset, limit=limit, filters=filters, order_by=JobMatch.final_score.desc()
        )
        total = await self.count(filters=filters)
        return list(items), total

    async def get_by_candidate(
        self, candidate_id: str, offset: int = 0, limit: int = 20
    ) -> tuple[list[JobMatch], int]:
        filters = {"candidate_id": candidate_id}
        items = await self.get_all(offset=offset, limit=limit, filters=filters)
        total = await self.count(filters=filters)
        return list(items), total

    async def get_match(self, job_id: str, candidate_id: str) -> JobMatch | None:
        stmt = select(JobMatch).where(
            JobMatch.job_id == job_id,
            JobMatch.candidate_id == candidate_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
