"""User service — manages user lifecycle."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UserRepository(session)

    async def get_or_create_from_clerk(self, clerk_payload: dict[str, Any]) -> User:
        """Get existing user or create from Clerk JWT payload."""
        clerk_id = clerk_payload.get("clerk_id") or clerk_payload.get("sub")
        email = clerk_payload.get("email")
        role = clerk_payload.get("role", "candidate")

        if not clerk_id or not email:
            raise ValueError("clerk_id and email are required")

        user = await self.repo.get_by_clerk_id(clerk_id)
        if user:
            user.last_login_at = datetime.now(UTC)
            return user

        user = await self.repo.create(
            clerk_id=clerk_id,
            email=email,
            role=role,
            last_login_at=datetime.now(UTC),
        )
        return user

    async def get_user(self, user_id: str) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_by_clerk_id(self, clerk_id: str) -> User | None:
        return await self.repo.get_by_clerk_id(clerk_id)

    async def update_user(self, user_id: str, **kwargs: Any) -> User:
        user = await self.get_user(user_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        return user
