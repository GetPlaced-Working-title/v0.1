"""SQLAlchemy models — import all here for Alembic auto-detection."""

from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.github_profile import GitHubProfile
from app.models.portfolio import Portfolio
from app.models.linkedin import LinkedInExport
from app.models.project import Project
from app.models.certificate import Certificate
from app.models.video import Video
from app.models.recommendation import Recommendation
from app.models.work_history import WorkHistory
from app.models.skill import Skill
from app.models.embedding import Embedding
from app.models.ai_score import AIAnalysisCache
from app.models.job_match import JobMatch
from app.models.notification import Notification
from app.models.audit_log import AuditLog

__all__ = [
    "User",
    "Company",
    "Job",
    "Candidate",
    "Resume",
    "GitHubProfile",
    "Portfolio",
    "LinkedInExport",
    "Project",
    "Certificate",
    "Video",
    "Recommendation",
    "WorkHistory",
    "Skill",
    "Embedding",
    "AIAnalysisCache",
    "JobMatch",
    "Notification",
    "AuditLog",
]
