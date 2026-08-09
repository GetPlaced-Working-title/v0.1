"""Certificate repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.certificate import Certificate
from app.repositories.base import BaseRepository


class CertificateRepository(BaseRepository[Certificate]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Certificate, session)

    async def get_by_candidate(self, candidate_id: str) -> list[Certificate]:
        stmt = (
            select(Certificate)
            .where(Certificate.candidate_id == candidate_id)
            .order_by(Certificate.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
