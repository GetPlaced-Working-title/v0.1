"""Skill schemas."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class SkillResponse(BaseModel):
    id: str
    candidate_id: str
    name: str
    category: str | None = None
    confidence: str = "resume_mention"
    evidence_sources: dict | None = None
    years_of_experience: Decimal | None = None
    last_used_date: date | None = None
    proficiency_level: str | None = None
    verified: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}
