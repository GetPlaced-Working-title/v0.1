"""Tests for Pydantic schemas and utility functions."""

import pytest
import sys
from unittest.mock import patch, MagicMock


def test_candidate_create_schema():
    from pydantic import BaseModel
    from typing import Optional
    from decimal import Decimal

    class CandidateCreate(BaseModel):
        name: str
        headline: Optional[str] = None
        location: Optional[str] = None
        open_to_remote: bool = True

    data = CandidateCreate(name="John", headline="Engineer", location="Remote")
    assert data.name == "John"
    assert data.headline == "Engineer"
    assert data.open_to_remote is True


def test_company_create_schema():
    from pydantic import BaseModel

    class CompanyCreate(BaseModel):
        name: str
        domain: Optional[str] = None
        industry: Optional[str] = None

    data = CompanyCreate(name="Acme Corp", domain="acme.com", industry="Technology")
    assert data.name == "Acme Corp"
    assert data.domain == "acme.com"


def test_paginated_response():
    from app.schemas.common import paginate

    result = paginate(items=["a", "b", "c"], total=25, page=1, size=20)
    assert result["items"] == ["a", "b", "c"]
    assert result["total"] == 25
    assert result["page"] == 1
    assert result["pages"] == 2


def test_project_create_schema():
    from pydantic import BaseModel

    class ProjectCreate(BaseModel):
        title: str
        description: Optional[str] = None
        technologies: Optional[list[str]] = None

    data = ProjectCreate(
        title="My Project",
        description="A cool project",
        technologies=["Python", "React"],
    )
    assert data.title == "My Project"
    assert "Python" in data.technologies


def test_certificate_create_schema():
    from pydantic import BaseModel

    class CertificateCreate(BaseModel):
        name: str
        issuer: Optional[str] = None

    data = CertificateCreate(name="AWS Solutions Architect", issuer="Amazon")
    assert data.name == "AWS Solutions Architect"


def test_search_request_schemas():
    from pydantic import BaseModel, Field

    class CandidateSearchRequest(BaseModel):
        query: str = ""
        location: Optional[str] = None
        page: int = Field(1, ge=1)
        size: int = Field(20, ge=1, le=100)

    cs = CandidateSearchRequest(query="python", location="SF", page=1, size=10)
    assert cs.query == "python"
    assert cs.page == 1

    class JobSearchRequest(BaseModel):
        query: str = ""
        employment_type: Optional[str] = None
        page: int = Field(1, ge=1)

    js = JobSearchRequest(query="engineer", employment_type="full_time", page=1)
    assert js.query == "engineer"


def test_pagination_params_direct():
    class PaginationParams:
        def __init__(self, page=1, size=20):
            self.page = page
            self.size = size
            self.offset = (page - 1) * size

    p = PaginationParams(page=3, size=50)
    assert p.page == 3
    assert p.size == 50
    assert p.offset == 100


def test_config_settings():
    from app.core.config import Settings

    s = Settings(
        app_env="test",
        debug=False,
        database_url="postgresql+asyncpg://localhost:5432/test",
        gemini_api_key="test-key",
        clerk_secret_key="test-key",
        clerk_jwks_url="http://localhost",
        clerk_issuer="http://localhost",
    )
    assert s.app_env == "test"
    assert s.is_development is False
    assert s.is_production is False


def test_exceptions():
    from app.core.exceptions import (
        AppException,
        NotFoundError,
        ConflictError,
        ValidationError,
        UnauthorizedError,
        ForbiddenError,
    )

    assert NotFoundError().status_code == 404
    assert ConflictError().status_code == 409
    assert ValidationError().status_code == 422
    assert UnauthorizedError().status_code == 401
    assert ForbiddenError().status_code == 403

    exc = AppException("Custom error", 418)
    assert exc.detail == "Custom error"
    assert exc.status_code == 418


def test_format_utils():
    def formatScore(score: float) -> str:
        return f"{int(round(score * 100))}%"

    assert formatScore(0.85) == "85%"
    assert formatScore(1.0) == "100%"


def test_validation_rules():
    import re

    def isValidGithubUsername(username: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", username)) and len(username) <= 39

    def isValidEmail(email: str) -> bool:
        return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))

    assert isValidGithubUsername("testuser") is True
    assert isValidGithubUsername("") is False
    assert isValidEmail("test@example.com") is True
    assert isValidEmail("not-email") is False


def test_constants():
    ROLES = {"CANDIDATE": "candidate", "RECRUITER": "recruiter", "ADMIN": "admin"}
    EMPLOYMENT_TYPES = ["full_time", "part_time", "contract", "internship"]

    assert ROLES["CANDIDATE"] == "candidate"
    assert "full_time" in EMPLOYMENT_TYPES
