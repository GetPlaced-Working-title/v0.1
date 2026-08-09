"""Generic CRUD repository base class."""

from __future__ import annotations

from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Generic repository with CRUD operations."""

    def __init__(self, model: Type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: str) -> ModelT | None:
        return await self.session.get(self.model, id)

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
        filters: dict[str, Any] | None = None,
        order_by: Any | None = None,
    ) -> Sequence[ModelT]:
        stmt = select(self.model)
        if filters:
            for key, value in filters.items():
                if value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            stmt = stmt.order_by(self.model.created_at.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        stmt = select(func.count()).select_from(self.model)
        if filters:
            for key, value in filters.items():
                if value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def create(self, **kwargs: Any) -> ModelT:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, id: str, **kwargs: Any) -> ModelT | None:
        instance = await self.get_by_id(id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, id: str) -> bool:
        instance = await self.get_by_id(id)
        if instance is None:
            return False
        if hasattr(instance, "deleted_at"):
            from datetime import datetime, timezone
            instance.deleted_at = datetime.now(timezone.utc)
        else:
            await self.session.delete(instance)
        await self.session.flush()
        return True

    async def exists(self, id: str) -> bool:
        stmt = select(func.count()).select_from(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one() > 0
