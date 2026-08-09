"""GitHub profile repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.github_profile import GitHubProfile
from app.repositories.base import BaseRepository


class GitHubProfileRepository(BaseRepository[GitHubProfile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(GitHubProfile, session)

    async def get_by_candidate(self, candidate_id: str) -> GitHubProfile | None:
        stmt = select(GitHubProfile).where(GitHubProfile.candidate_id == candidate_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> GitHubProfile | None:
        stmt = select(GitHubProfile).where(GitHubProfile.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
