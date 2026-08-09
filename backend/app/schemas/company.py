"""Company schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    domain: str | None = None
    website: str | None = None
    industry: str | None = None
    size: str | None = None
    description: str | None = None
    location: str | None = None


class CompanyUpdate(BaseModel):
    name: str | None = None
    domain: str | None = None
    website: str | None = None
    industry: str | None = None
    size: str | None = None
    description: str | None = None
    logo_url: str | None = None
    location: str | None = None


class CompanyResponse(BaseModel):
    id: str
    user_id: str
    name: str
    domain: str | None = None
    website: str | None = None
    industry: str | None = None
    size: str | None = None
    description: str | None = None
    logo_url: str | None = None
    location: str | None = None
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
