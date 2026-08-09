"""Job repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Job, session)

    async def get_by_company(
        self, company_id: str, offset: int = 0, limit: int = 20
    ) -> tuple[list[Job], int]:
        filters = {"company_id": company_id}
        items = await self.get_all(offset=offset, limit=limit, filters=filters)
        total = await self.count(filters=filters)
        return list(items), total

    async def get_active_jobs(
        self, offset: int = 0, limit: int = 20
    ) -> tuple[list[Job], int]:
        filters = {"status": "active"}
        items = await self.get_all(offset=offset, limit=limit, filters=filters)
        total = await self.count(filters=filters)
        return list(items), total

    async def search(
        self,
        query: str | None = None,
        location: str | None = None,
        employment_type: str | None = None,
        work_mode: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Job], int]:
        stmt = select(Job).where(Job.status == "active")
        count_base = select(Job).where(Job.status == "active")

        if query:
            like = f"%{query}%"
            condition = Job.title.ilike(like) | Job.description.ilike(like)
            stmt = stmt.where(condition)
            count_base = count_base.where(condition)
        if location:
            stmt = stmt.where(Job.location.ilike(f"%{location}%"))
            count_base = count_base.where(Job.location.ilike(f"%{location}%"))
        if employment_type:
            stmt = stmt.where(Job.employment_type == employment_type)
            count_base = count_base.where(Job.employment_type == employment_type)
        if work_mode:
            stmt = stmt.where(Job.work_mode == work_mode)
            count_base = count_base.where(Job.work_mode == work_mode)

        total_result = await self.session.execute(
            select(Job.id).select_from(count_base.subquery())
        )
        total = len(total_result.all())

        stmt = stmt.order_by(Job.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total
