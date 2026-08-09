"""Candidate service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.candidate import Candidate
from app.repositories.candidate import CandidateRepository


class CandidateService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CandidateRepository(session)

    async def create_candidate(self, user_id: str, **kwargs) -> Candidate:
        existing = await self.repo.get_by_user_id(user_id)
        if existing:
            raise ConflictError("Candidate profile already exists")
        return await self.repo.create(user_id=user_id, **kwargs)

    async def get_candidate(self, candidate_id: str) -> Candidate:
        candidate = await self.repo.get_by_id(candidate_id)
        if not candidate:
            raise NotFoundError("Candidate not found")
        return candidate

    async def get_by_user_id(self, user_id: str) -> Candidate | None:
        return await self.repo.get_by_user_id(user_id)

    async def update_candidate(self, candidate_id: str, **kwargs) -> Candidate:
        candidate = await self.get_candidate(candidate_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(candidate, key, value)
        return candidate

    async def update_profile_scores(
        self, candidate_id: str, scores: dict, summary: dict, confidence: str
    ) -> Candidate:
        return await self.update_candidate(
            candidate_id,
            overall_scores=scores,
            profile_summary=summary,
            evidence_confidence=confidence,
        )

    async def search_candidates(self, **kwargs):
        return await self.repo.search(**kwargs)

    async def list_candidates(self, offset: int = 0, limit: int = 20):
        items = await self.repo.get_all(offset=offset, limit=limit)
        total = await self.repo.count()
        return list(items), total
