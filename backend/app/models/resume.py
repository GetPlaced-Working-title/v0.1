"""Resume model with AI analysis results."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Resume(Base, TimestampMixin, SoftDeleteMixin):
    """Uploaded resume with parsed and analyzed content."""

    __tablename__ = "resumes"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Parsed structured data
    basic_info: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    experience: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    education: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    skills_extracted: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    projects_extracted: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    certifications_extracted: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    achievements: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    languages: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    publications: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    awards: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # AI analysis
    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    resume_quality: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    consistency_flags: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    missing_info: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ats_compatibility: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Status
    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="resumes")
