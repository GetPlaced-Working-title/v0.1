"""Job posting model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import ARRAY, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Job(Base, TimestampMixin, SoftDeleteMixin):
    """Job posting by a company."""

    __tablename__ = "jobs"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    responsibilities: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    required_skills: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    preferred_skills: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    experience_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    experience_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    education_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    employment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    work_mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(10), default="USD")
    benefits: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    embedding_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    applications_count: Mapped[int] = mapped_column(Integer, default=0)
    matches_count: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="jobs")
    matches = relationship("JobMatch", back_populates="job")
