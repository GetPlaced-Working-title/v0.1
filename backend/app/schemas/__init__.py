"""Pydantic schemas for request/response validation."""

from app.schemas.common import ErrorResponse, MessageResponse, PaginatedResponse, paginate
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.schemas.job import JobCreate, JobListResponse, JobResponse, JobUpdate
from app.schemas.candidate import (
    CandidateCreate,
    CandidateListResponse,
    CandidateResponse,
    CandidateUpdate,
)
from app.schemas.resume import ResumeResponse, ResumeUploadResponse
from app.schemas.github import GitHubConnect, GitHubProfileResponse
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.certificate import CertificateCreate, CertificateResponse
from app.schemas.video import VideoResponse, VideoUploadResponse
from app.schemas.recommendation import RecommendationCreate, RecommendationResponse
from app.schemas.work_history import WorkHistoryCreate, WorkHistoryResponse
from app.schemas.skill import SkillResponse
from app.schemas.search import (
    CandidateSearchRequest,
    JobSearchRequest,
    MatchRequest,
    MatchResponse,
    MatchResult,
)
from app.schemas.matching import JobMatchResponse, MatchStatusUpdate

__all__ = [
    "ErrorResponse",
    "MessageResponse",
    "PaginatedResponse",
    "paginate",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    "CompanyCreate",
    "CompanyResponse",
    "CompanyUpdate",
    "JobCreate",
    "JobListResponse",
    "JobResponse",
    "JobUpdate",
    "CandidateCreate",
    "CandidateListResponse",
    "CandidateResponse",
    "CandidateUpdate",
    "ResumeResponse",
    "ResumeUploadResponse",
    "GitHubConnect",
    "GitHubProfileResponse",
    "PortfolioCreate",
    "PortfolioResponse",
    "ProjectCreate",
    "ProjectResponse",
    "ProjectUpdate",
    "CertificateCreate",
    "CertificateResponse",
    "VideoResponse",
    "VideoUploadResponse",
    "RecommendationCreate",
    "RecommendationResponse",
    "WorkHistoryCreate",
    "WorkHistoryResponse",
    "SkillResponse",
    "CandidateSearchRequest",
    "JobSearchRequest",
    "MatchRequest",
    "MatchResponse",
    "MatchResult",
    "JobMatchResponse",
    "MatchStatusUpdate",
]
