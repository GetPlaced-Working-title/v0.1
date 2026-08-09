"""Resume service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.storage import StorageService
from app.models.resume import Resume
from app.repositories.resume import ResumeRepository


class ResumeService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ResumeRepository(session)
        self.storage = StorageService()

    async def upload_resume(
        self,
        candidate_id: str,
        file_data: bytes,
        file_name: str,
        file_type: str,
    ) -> Resume:
        key = StorageService.generate_key("resumes", file_name, candidate_id)
        self.storage.upload_file(file_data, key, content_type=file_type)

        existing_resumes = await self.repo.get_by_candidate(candidate_id)
        is_primary = len(existing_resumes) == 0

        resume = await self.repo.create(
            candidate_id=candidate_id,
            file_url=self.storage.get_file_url(key),
            file_name=file_name,
            file_size=len(file_data),
            file_type=file_type,
            is_primary=is_primary,
            processing_status="pending",
        )
        return resume

    async def get_resume(self, resume_id: str) -> Resume:
        resume = await self.repo.get_by_id(resume_id)
        if not resume:
            raise NotFoundError("Resume not found")
        return resume

    async def list_resumes(self, candidate_id: str) -> list[Resume]:
        return await self.repo.get_by_candidate(candidate_id)

    async def update_analysis(self, resume_id: str, **kwargs) -> Resume:
        resume = await self.get_resume(resume_id)
        for key, value in kwargs.items():
            setattr(resume, key, value)
        return resume
