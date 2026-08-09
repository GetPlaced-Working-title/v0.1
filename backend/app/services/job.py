"""Job service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.job import Job
from app.repositories.job import JobRepository


class JobService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = JobRepository(session)

    async def create_job(self, company_id: str, **kwargs) -> Job:
        return await self.repo.create(company_id=company_id, status="draft", **kwargs)

    async def get_job(self, job_id: str) -> Job:
        job = await self.repo.get_by_id(job_id)
        if not job:
            raise NotFoundError("Job not found")
        return job

    async def update_job(self, job_id: str, **kwargs) -> Job:
        job = await self.get_job(job_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(job, key, value)
        return job

    async def publish_job(self, job_id: str) -> Job:
        return await self.update_job(job_id, status="active")

    async def close_job(self, job_id: str) -> Job:
        return await self.update_job(job_id, status="closed")

    async def list_by_company(self, company_id: str, offset: int = 0, limit: int = 20):
        return await self.repo.get_by_company(company_id, offset=offset, limit=limit)

    async def list_active(self, offset: int = 0, limit: int = 20):
        return await self.repo.get_active_jobs(offset=offset, limit=limit)

    async def search_jobs(self, **kwargs):
        return await self.repo.search(**kwargs)
