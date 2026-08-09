"""Recommendation schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class RecommendationCreate(BaseModel):
    recommender_name: str | None = None
    recommender_title: str | None = None
    recommender_company: str | None = None
    relationship: str | None = None
    content: str | None = None


class RecommendationResponse(BaseModel):
    id: str
    candidate_id: str
    recommender_name: str | None = None
    recommender_title: str | None = None
    recommender_company: str | None = None
    relationship: str | None = None
    content: str | None = None
    file_url: str | None = None
    analysis: dict | None = None
    scores: dict | None = None
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
