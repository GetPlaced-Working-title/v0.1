"""Candidate schemas."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CandidateCreate(BaseModel):
    name: str
    headline: str | None = None
    location: str | None = None
    phone: str | None = None
    bio: str | None = None
    preferred_roles: list[str] | None = None
    preferred_locations: list[str] | None = None
    open_to_remote: bool = True
    salary_expectation_min: int | None = None
    salary_expectation_max: int | None = None
    salary_currency: str = "USD"
    availability: str | None = None


class CandidateUpdate(BaseModel):
    name: str | None = None
    headline: str | None = None
    location: str | None = None
    phone: str | None = None
    bio: str | None = None
    current_role: str | None = None
    current_company: str | None = None
    preferred_roles: list[str] | None = None
    preferred_locations: list[str] | None = None
    open_to_remote: bool | None = None
    salary_expectation_min: int | None = None
    salary_expectation_max: int | None = None
    salary_currency: str | None = None
    availability: str | None = None


class CandidateResponse(BaseModel):
    id: str
    user_id: str
    name: str
    headline: str | None = None
    location: str | None = None
    phone: str | None = None
    bio: str | None = None
    years_of_experience: Decimal | None = None
    current_role: str | None = None
    current_company: str | None = None
    preferred_roles: list[str] | None = None
    preferred_locations: list[str] | None = None
    open_to_remote: bool = True
    salary_expectation_min: int | None = None
    salary_expectation_max: int | None = None
    salary_currency: str = "USD"
    availability: str | None = None
    profile_completeness: int = 0
    evidence_confidence: str = "none"
    profile_summary: dict | None = None
    overall_scores: dict | None = None
    last_analyzed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CandidateListResponse(BaseModel):
    id: str
    name: str
    headline: str | None = None
    location: str | None = None
    years_of_experience: Decimal | None = None
    current_role: str | None = None
    evidence_confidence: str = "none"
    profile_completeness: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}
