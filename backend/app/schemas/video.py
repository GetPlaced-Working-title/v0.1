"""Video schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class VideoResponse(BaseModel):
    id: str
    candidate_id: str
    title: str | None = None
    description: str | None = None
    file_url: str
    duration_seconds: int | None = None
    file_size: int | None = None
    thumbnail_url: str | None = None
    transcript: str | None = None
    analysis: dict | None = None
    scores: dict | None = None
    processing_status: str = "pending"
    analyzed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class VideoUploadResponse(BaseModel):
    id: str
    file_url: str
    processing_status: str = "pending"
    message: str = "Video uploaded. Analysis will begin shortly."
