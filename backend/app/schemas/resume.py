"""Resume schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: str
    candidate_id: str
    file_url: str
    file_name: str | None = None
    file_size: int | None = None
    file_type: str | None = None
    basic_info: dict | None = None
    experience: dict | None = None
    education: dict | None = None
    skills_extracted: dict | None = None
    analysis: dict | None = None
    scores: dict | None = None
    resume_quality: dict | None = None
    processing_status: str = "pending"
    is_primary: bool = False
    version: int = 1
    analyzed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeUploadResponse(BaseModel):
    id: str
    file_url: str
    processing_status: str = "pending"
    message: str = "Resume uploaded. Analysis will begin shortly."
