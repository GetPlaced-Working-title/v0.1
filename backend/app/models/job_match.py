"""Job match model."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class JobMatch(Base, TimestampMixin):
    """Match between a job and a candidate with scoring breakdown."""

    __tablename__ = "job_matches"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_id", name="uq_job_matches_job_candidate"),
    )

    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    vector_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    keyword_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    hybrid_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    rerank_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    final_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    match_details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    strengths: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    gaps: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    interview_questions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="matched")
    recruiter_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    job = relationship("Job", back_populates="matches")
    candidate = relationship("Candidate", back_populates="matches")
