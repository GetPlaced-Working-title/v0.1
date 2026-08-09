"""Certificate schemas."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class CertificateCreate(BaseModel):
    name: str
    issuer: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    difficulty_level: str | None = None
    assessment_type: str | None = None
    learning_hours: float | None = None
    skills_covered: list[str] | None = None


class CertificateResponse(BaseModel):
    id: str
    candidate_id: str
    name: str
    issuer: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    file_url: str | None = None
    difficulty_level: str | None = None
    assessment_type: str | None = None
    skills_covered: list[str] | None = None
    analysis: dict | None = None
    scores: dict | None = None
    is_verified: bool = False
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
