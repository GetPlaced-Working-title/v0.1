"""Video repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import Video
from app.repositories.base import BaseRepository


class VideoRepository(BaseRepository[Video]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Video, session)

    async def get_by_candidate(self, candidate_id: str) -> list[Video]:
        stmt = (
            select(Video)
            .where(Video.candidate_id == candidate_id)
            .order_by(Video.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
