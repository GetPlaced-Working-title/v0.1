"""GitHub profile model with AI analysis."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class GitHubProfile(Base, TimestampMixin, SoftDeleteMixin):
    """GitHub profile with analyzed repositories and coding patterns."""

    __tablename__ = "github_profiles"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    account_age_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    public_repos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    followers: Mapped[int | None] = mapped_column(Integer, nullable=True)
    following: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_stars: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_forks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    contribution_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    primary_languages: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    repositories: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # AI analysis
    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    skill_verification: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ai_code_detection: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Status
    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="github_profile")
