"""GitHub service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.github_profile import GitHubProfile
from app.repositories.github import GitHubProfileRepository


class GitHubService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = GitHubProfileRepository(session)

    async def connect_github(self, candidate_id: str, username: str) -> GitHubProfile:
        existing = await self.repo.get_by_candidate(candidate_id)
        if existing:
            existing.username = username
            existing.processing_status = "pending"
            return existing
        return await self.repo.create(
            candidate_id=candidate_id,
            username=username,
            profile_url=f"https://github.com/{username}",
            processing_status="pending",
        )

    async def get_profile(self, candidate_id: str) -> GitHubProfile:
        profile = await self.repo.get_by_candidate(candidate_id)
        if not profile:
            raise NotFoundError("GitHub profile not connected")
        return profile

    async def update_analysis(self, profile_id: str, **kwargs) -> GitHubProfile:
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            raise NotFoundError("GitHub profile not found")
        for key, value in kwargs.items():
            setattr(profile, key, value)
        return profile
