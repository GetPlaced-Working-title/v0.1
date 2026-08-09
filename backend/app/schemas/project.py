"""Project schemas."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    role: str | None = None
    technologies: list[str] | None = None
    url: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_ongoing: bool = False
    scope: str | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    role: str | None = None
    technologies: list[str] | None = None
    url: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_ongoing: bool | None = None
    scope: str | None = None


class ProjectResponse(BaseModel):
    id: str
    candidate_id: str
    title: str
    description: str | None = None
    role: str | None = None
    technologies: list[str] | None = None
    url: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_ongoing: bool = False
    scope: str | None = None
    analysis: dict | None = None
    scores: dict | None = None
    source: str | None = None
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
