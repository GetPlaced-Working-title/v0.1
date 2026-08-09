"""Job schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str
    description: str
    requirements: dict | None = None
    responsibilities: list[str] | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    experience_min: int | None = None
    experience_max: int | None = None
    education_level: str | None = None
    employment_type: str | None = None
    work_mode: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str = "USD"
    benefits: list[str] | None = None
    expires_at: datetime | None = None


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    requirements: dict | None = None
    responsibilities: list[str] | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    experience_min: int | None = None
    experience_max: int | None = None
    education_level: str | None = None
    employment_type: str | None = None
    work_mode: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    benefits: list[str] | None = None
    status: str | None = None
    expires_at: datetime | None = None


class JobResponse(BaseModel):
    id: str
    company_id: str
    title: str
    description: str
    requirements: dict | None = None
    responsibilities: list[str] | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    experience_min: int | None = None
    experience_max: int | None = None
    education_level: str | None = None
    employment_type: str | None = None
    work_mode: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str = "USD"
    benefits: list[str] | None = None
    status: str = "draft"
    applications_count: int = 0
    matches_count: int = 0
    expires_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    id: str
    company_id: str
    title: str
    required_skills: list[str] | None = None
    employment_type: str | None = None
    work_mode: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    status: str = "draft"
    matches_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}
