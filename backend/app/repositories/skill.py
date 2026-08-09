"""Skill repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.repositories.base import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Skill, session)

    async def get_by_candidate(self, candidate_id: str) -> list[Skill]:
        stmt = (
            select(Skill)
            .where(Skill.candidate_id == candidate_id)
            .order_by(Skill.confidence.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def upsert_skill(
        self,
        candidate_id: str,
        name: str,
        **kwargs,
    ) -> Skill:
        stmt = select(Skill).where(
            Skill.candidate_id == candidate_id,
            Skill.name == name,
        )
        result = await self.session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(existing, key, value)
            return existing
        skill = Skill(candidate_id=candidate_id, name=name, **kwargs)
        self.session.add(skill)
        return skill
