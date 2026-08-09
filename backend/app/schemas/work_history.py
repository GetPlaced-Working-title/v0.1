"""Work history schemas."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class WorkHistoryCreate(BaseModel):
    company: str
    title: str
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    employment_type: str | None = None
    description: str | None = None
    responsibilities: list[str] | None = None
    achievements: list[str] | None = None
    technologies: list[str] | None = None


class WorkHistoryResponse(BaseModel):
    id: str
    candidate_id: str
    company: str
    title: str
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    employment_type: str | None = None
    description: str | None = None
    responsibilities: list[str] | None = None
    achievements: list[str] | None = None
    technologies: list[str] | None = None
    analysis: dict | None = None
    scores: dict | None = None
    source: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
