"""LinkedIn schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class LinkedInResponse(BaseModel):
    id: str
    candidate_id: str
    file_url: str | None = None
    profile_url: str | None = None
    headline: str | None = None
    about: str | None = None
    experience: dict | None = None
    education: dict | None = None
    skills: dict | None = None
    analysis: dict | None = None
    scores: dict | None = None
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
