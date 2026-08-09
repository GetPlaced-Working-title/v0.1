"""Matching schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class JobMatchResponse(BaseModel):
    id: str
    job_id: str
    candidate_id: str
    vector_score: float | None = None
    keyword_score: float | None = None
    hybrid_score: float | None = None
    rerank_score: float | None = None
    final_score: float | None = None
    rank: int | None = None
    match_details: dict | None = None
    strengths: dict | None = None
    gaps: dict | None = None
    interview_questions: dict | None = None
    status: str = "matched"
    recruiter_notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MatchStatusUpdate(BaseModel):
    status: str
    recruiter_notes: str | None = None
