"""Repository layer — data access objects."""

from app.repositories.base import BaseRepository
from app.repositories.candidate import CandidateRepository
from app.repositories.certificate import CertificateRepository
from app.repositories.company import CompanyRepository
from app.repositories.github import GitHubProfileRepository
from app.repositories.job import JobRepository
from app.repositories.job_match import JobMatchRepository
from app.repositories.portfolio import PortfolioRepository
from app.repositories.project import ProjectRepository
from app.repositories.resume import ResumeRepository
from app.repositories.skill import SkillRepository
from app.repositories.user import UserRepository
from app.repositories.video import VideoRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "CompanyRepository",
    "CandidateRepository",
    "JobRepository",
    "ResumeRepository",
    "GitHubProfileRepository",
    "PortfolioRepository",
    "ProjectRepository",
    "CertificateRepository",
    "VideoRepository",
    "SkillRepository",
    "JobMatchRepository",
]
