"""Search and matching schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CandidateSearchRequest(BaseModel):
    query: str = ""
    location: str | None = None
    min_experience: int | None = None
    max_experience: int | None = None
    skills: list[str] | None = None
    availability: str | None = None
    open_to_remote: bool | None = None
    evidence_confidence: str | None = None
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)


class JobSearchRequest(BaseModel):
    query: str = ""
    location: str | None = None
    employment_type: str | None = None
    work_mode: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    skills: list[str] | None = None
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)


class MatchRequest(BaseModel):
    job_id: str
    top_k: int = Field(10, ge=1, le=50)


class MatchResult(BaseModel):
    candidate_id: str
    candidate_name: str
    final_score: float
    vector_score: float | None = None
    keyword_score: float | None = None
    rerank_score: float | None = None
    match_details: dict | None = None
    strengths: dict | None = None
    gaps: dict | None = None


class MatchResponse(BaseModel):
    job_id: str
    matches: list[MatchResult]
    total_candidates_evaluated: int
