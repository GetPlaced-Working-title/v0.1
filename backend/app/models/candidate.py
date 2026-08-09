"""Candidate profile model."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import ARRAY, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Candidate(Base, TimestampMixin, SoftDeleteMixin):
    """Candidate profile — the core entity the AI builds evidence for."""

    __tablename__ = "candidates"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    headline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    years_of_experience: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)
    current_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    preferred_roles: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    preferred_locations: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    open_to_remote: Mapped[bool] = mapped_column(Boolean, default=True)
    salary_expectation_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_expectation_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(10), default="USD")
    availability: Mapped[str | None] = mapped_column(String(50), nullable=True)
    profile_completeness: Mapped[int] = mapped_column(Integer, default=0)
    evidence_confidence: Mapped[str] = mapped_column(String(50), default="none")
    profile_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    overall_scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    profile_embedding_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_analyzed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user = relationship("User", back_populates="candidate")
    resumes = relationship("Resume", back_populates="candidate")
    github_profile = relationship("GitHubProfile", back_populates="candidate", uselist=False)
    portfolios = relationship("Portfolio", back_populates="candidate")
    linkedin_export = relationship("LinkedInExport", back_populates="candidate", uselist=False)
    projects = relationship("Project", back_populates="candidate")
    certificates = relationship("Certificate", back_populates="candidate")
    videos = relationship("Video", back_populates="candidate")
    recommendations = relationship("Recommendation", back_populates="candidate")
    work_history = relationship("WorkHistory", back_populates="candidate")
    skills = relationship("Skill", back_populates="candidate")
    matches = relationship("JobMatch", back_populates="candidate")
