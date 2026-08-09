"""Celery application configuration."""

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "talent_ai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_soft_time_limit=300,
    task_time_limit=600,
    result_expires=86400,
    task_routes={
        "app.tasks.resume.*": {"queue": "ai_analysis"},
        "app.tasks.github.*": {"queue": "ai_analysis"},
        "app.tasks.portfolio.*": {"queue": "ai_analysis"},
        "app.tasks.linkedin.*": {"queue": "ai_analysis"},
        "app.tasks.video.*": {"queue": "ai_analysis"},
        "app.tasks.certificate.*": {"queue": "ai_analysis"},
        "app.tasks.embedding.*": {"queue": "embeddings"},
        "app.tasks.profile.*": {"queue": "ai_analysis"},
        "app.tasks.matching.*": {"queue": "matching"},
    },
)

celery_app.autodiscover_tasks(
    [
        "app.tasks.resume",
        "app.tasks.github",
        "app.tasks.portfolio",
        "app.tasks.linkedin",
        "app.tasks.video",
        "app.tasks.certificate",
        "app.tasks.embedding",
        "app.tasks.profile",
        "app.tasks.matching",
    ]
)
