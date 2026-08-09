"""GitHub profile schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class GitHubConnect(BaseModel):
    username: str


class GitHubProfileResponse(BaseModel):
    id: str
    candidate_id: str
    username: str
    profile_url: str | None = None
    account_age_days: int | None = None
    public_repos: int | None = None
    followers: int | None = None
    total_stars: int | None = None
    total_forks: int | None = None
    primary_languages: dict | None = None
    repositories: dict | None = None
    analysis: dict | None = None
    scores: dict | None = None
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
