"""Portfolio schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    url: str
    title: str | None = None
    portfolio_type: str | None = None


class PortfolioResponse(BaseModel):
    id: str
    candidate_id: str
    url: str
    title: str | None = None
    portfolio_type: str | None = None
    projects_found: dict | None = None
    analysis: dict | None = None
    scores: dict | None = None
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
