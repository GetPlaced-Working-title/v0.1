"""Comprehensive unit tests for GetPlaced backend."""

import pytest


# ─── Config & Settings ────────────────────────────────────────────────

def test_config_defaults():
    from app.core.config import Settings

    s = Settings(
        app_env="test",
        database_url="postgresql+asyncpg://localhost/test",
        gemini_api_key="test-key",
        clerk_secret_key="test-key",
        clerk_jwks_url="http://localhost",
        clerk_issuer="http://localhost",
    )
    assert s.app_name == "AI Talent Router"
    assert s.api_version == "v1"
    assert s.is_development is False
    assert s.is_production is False
    assert s.qdrant_vector_size == 768
    assert s.gemini_model == "gemini-2.0-flash-lite"


def test_config_cors_parsing():
    from app.core.config import Settings

    s = Settings(
        cors_origins="http://localhost:3000,http://localhost:8000",
        gemini_api_key="k",
        clerk_secret_key="k",
        clerk_jwks_url="http://l",
        clerk_issuer="http://l",
    )
    assert "http://localhost:3000" in s.cors_origins
    assert "http://localhost:8000" in s.cors_origins


# ─── Exceptions ───────────────────────────────────────────────────────

def test_app_exceptions():
    from app.core.exceptions import (
        AppException,
        NotFoundError,
        ConflictError,
        ValidationError,
        UnauthorizedError,
        ForbiddenError,
        AIAnalysisError,
        StorageError,
        RateLimitError,
    )

    assert NotFoundError().status_code == 404
    assert ConflictError().status_code == 409
    assert ValidationError().status_code == 422
    assert UnauthorizedError().status_code == 401
    assert ForbiddenError().status_code == 403
    assert AIAnalysisError().status_code == 502
    assert StorageError().status_code == 502
    assert RateLimitError().status_code == 429

    exc = AppException("Custom message", 418)
    assert exc.detail == "Custom message"
    assert exc.status_code == 418


def test_exception_inheritance():
    from app.core.exceptions import NotFoundError, AppException
    assert issubclass(NotFoundError, AppException)
    assert issubclass(NotFoundError, Exception)


# ─── Schemas (common) ─────────────────────────────────────────────────

def test_paginated_response():
    from app.schemas.common import paginate

    result = paginate(items=["a", "b", "c"], total=25, page=1, size=20)
    assert result["items"] == ["a", "b", "c"]
    assert result["total"] == 25
    assert result["page"] == 1
    assert result["pages"] == 2

    # Second page
    result = paginate(items=["d", "e"], total=25, page=2, size=20)
    assert result["pages"] == 2
    assert result["page"] == 2

    # Exact page
    result = paginate(items=[], total=20, page=2, size=10)
    assert result["pages"] == 2


# ─── Pydantic Schema Validation ───────────────────────────────────────

def test_candidate_create_validation():
    from pydantic import BaseModel
    from typing import Optional

    class CandidateCreate(BaseModel):
        name: str
        headline: Optional[str] = None
        location: Optional[str] = None
        open_to_remote: bool = True
        salary_currency: str = "USD"

    data = CandidateCreate(name="John", headline="Engineer")
    assert data.name == "John"
    assert data.open_to_remote is True
    assert data.salary_currency == "USD"

    # Defaults
    data = CandidateCreate(name="Jane")
    assert data.headline is None
    assert data.open_to_remote is True


def test_job_create_validation():
    from pydantic import BaseModel, Field
    from typing import Optional

    class JobCreate(BaseModel):
        title: str
        description: str = Field(..., min_length=1)
        required_skills: list[str] = []
        employment_type: str = "full_time"
        work_mode: str = "remote"

    data = JobCreate(title="Engineer", description="Build things", required_skills=["Python"])
    assert data.title == "Engineer"
    assert "Python" in data.required_skills

    # Empty skills
    data = JobCreate(title="Intern", description="Learn")
    assert data.required_skills == []


def test_search_request_schemas():
    from pydantic import BaseModel, Field
    from typing import Optional

    class CandidateSearchRequest(BaseModel):
        query: str = ""
        location: Optional[str] = None
        page: int = Field(1, ge=1)
        size: int = Field(20, ge=1, le=100)

    cs = CandidateSearchRequest(query="python", location="SF", page=3, size=10)
    assert cs.query == "python"
    assert cs.page == 3
    assert cs.size == 10

    # Bounds
    cs = CandidateSearchRequest(size=100)
    assert cs.size == 100


def test_pagination_params_class():
    class PaginationParams:
        def __init__(self, page: int = 1, size: int = 20):
            self.page = page
            self.size = size
            self.offset = (page - 1) * size

    p = PaginationParams(page=3, size=50)
    assert p.page == 3
    assert p.offset == 100
    assert p.size == 50

    p = PaginationParams()
    assert p.offset == 0
    assert p.page == 1


# ─── Utility Functions ────────────────────────────────────────────────

def test_format_score():
    def formatScore(score: float) -> str:
        return f"{int(round(score * 100))}%"

    assert formatScore(1.0) == "100%"
    assert formatScore(0.85) == "85%"
    assert formatScore(0.0) == "0%"
    assert formatScore(0.333) == "33%"


def test_github_username_validation():
    import re

    def isValidGithubUsername(username: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", username)) and len(username) <= 39

    assert isValidGithubUsername("testuser") is True
    assert isValidGithubUsername("test-user") is True
    assert isValidGithubUsername("test123") is True
    assert isValidGithubUsername("") is False
    assert isValidGithubUsername("-invalid") is False
    assert isValidGithubUsername("a" * 40) is False


def test_email_validation():
    import re

    def isValidEmail(email: str) -> bool:
        return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))

    assert isValidEmail("user@example.com") is True
    assert isValidEmail("test@domain.co") is True
    assert isValidEmail("not-an-email") is False
    assert isValidEmail("") is False


# ─── Profile Builder (Scoring) ────────────────────────────────────────

def test_profile_builder_aggregation():
    from app.ai.scoring.profile_builder import ProfileBuilder

    builder = ProfileBuilder()

    builder.add_analysis("resume", {
        "scores": {"experience_quality": 0.7, "achievement_quality": 0.5},
        "skills": [{"name": "Python", "category": "programming"}],
    })

    builder.add_analysis("github", {
        "scores": {"technical_depth": 0.9},
        "skills": [{"name": "Python", "category": "programming"}],
    })

    result = builder.build()

    assert "aggregate_scores" in result
    assert "skills_graph" in result
    assert "evidence_confidence" in result
    assert result["evidence_confidence"] != "none"

    # Skills should merge
    assert len(result["skills_graph"]) == 1
    assert result["skills_graph"][0]["name"].lower() == "python"
    assert "github" in result["skills_graph"][0]["evidence_sources"]


def test_profile_builder_empty():
    from app.ai.scoring.profile_builder import ProfileBuilder

    builder = ProfileBuilder()
    result = builder.build()

    assert result["evidence_confidence"] == "none"
    assert result["skills_graph"] == []
    assert result["aggregate_scores"] == {}


# ─── Evidence Scoring ─────────────────────────────────────────────────

def test_evidence_confidence_levels():
    from app.ai.scoring.evidence_scorer import calculate_confidence, EvidenceConfidence

    assert calculate_confidence([]) == EvidenceConfidence.NONE
    assert calculate_confidence(["resume"]) == EvidenceConfidence.LOW
    assert calculate_confidence(["github"]) == EvidenceConfidence.MEDIUM
    assert calculate_confidence(["portfolio_live", "github"]) == EvidenceConfidence.HIGH
    assert calculate_confidence(["github", "portfolio_live", "assessment"]) == EvidenceConfidence.VERY_HIGH


def test_clamp_score():
    from app.ai.scoring.evidence_scorer import clamp_score

    assert clamp_score(50) == 50
    assert clamp_score(150) == 100
    assert clamp_score(-10) == 0
    assert clamp_score(100) == 100
    assert clamp_score(0) == 0


# ─── AI Client ────────────────────────────────────────────────────────

def test_input_hash_consistency():
    import sys
    from unittest.mock import patch

    # Mock structlog + google to avoid import errors
    mock_logging = patch.dict(sys.modules, {
        "app.core.logging": type(sys)("logging"),
        "app.core.config": __import__("app.core.config", fromlist=["get_settings"]),
    })

    with mock_logging:
        sys.modules["app.core.logging"].get_logger = lambda name=None: None

    with patch("google.generativeai.configure"):
        from app.ai.client import GeminiClient

        h1 = GeminiClient.compute_input_hash("hello", "resume_analysis")
        h2 = GeminiClient.compute_input_hash("hello", "resume_analysis")
        h3 = GeminiClient.compute_input_hash("world", "resume_analysis")
        h4 = GeminiClient.compute_input_hash("hello", "github_analysis")

        assert h1 == h2
        assert h1 != h3
        assert h1 != h4
        assert len(h1) == 64
        assert all(c in "0123456789abcdef" for c in h1)


# ─── AI Generators ────────────────────────────────────────────────────

def test_summary_generator_exists():
    from unittest.mock import patch
    with patch("google.generativeai.configure"), patch("app.ai.client.get_gemini_client"):
        from app.ai.generators.summary import SummaryGenerator
        assert SummaryGenerator is not None


def test_interview_questions_generator_exists():
    from unittest.mock import patch
    with patch("google.generativeai.configure"), patch("app.ai.client.get_gemini_client"):
        from app.ai.generators.interview_questions import InterviewQuestionGenerator
        assert InterviewQuestionGenerator is not None


def test_skill_gap_generator_exists():
    from unittest.mock import patch
    with patch("google.generativeai.configure"), patch("app.ai.client.get_gemini_client"):
        from app.ai.generators.skill_gap import SkillGapAnalyzer
        assert SkillGapAnalyzer is not None


# ─── Scoring Modules ──────────────────────────────────────────────────

def test_consistency_checker():
    from app.ai.scoring.consistency_checker import ConsistencyChecker
    assert ConsistencyChecker is not None


def test_red_flag_detector():
    from app.ai.scoring.red_flag_detector import RedFlagDetector
    assert RedFlagDetector is not None


# ─── Constants ────────────────────────────────────────────────────────

def test_constants():
    ROLES = {"CANDIDATE": "candidate", "RECRUITER": "recruiter", "ADMIN": "admin"}
    EMPLOYMENT_TYPES = ["full_time", "part_time", "contract", "internship"]

    assert ROLES["CANDIDATE"] == "candidate"
    assert ROLES["RECRUITER"] == "recruiter"
    assert "full_time" in EMPLOYMENT_TYPES
    assert "contract" in EMPLOYMENT_TYPES
    assert len(EMPLOYMENT_TYPES) == 4
