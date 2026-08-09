"""User schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    role: str = Field("candidate", pattern="^(candidate|recruiter|admin)$")


class UserCreate(UserBase):
    clerk_id: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: str
    clerk_id: str
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
