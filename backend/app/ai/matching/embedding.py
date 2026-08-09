"""Embedding generation for candidates and jobs."""

from __future__ import annotations

from typing import Any

from app.ai.client import get_gemini_client
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.qdrant import QdrantService

logger = get_logger(__name__)
settings = get_settings()


def build_candidate_embedding_text(profile: dict[str, Any]) -> str:
    """Turn a candidate profile into optimized embedding input text."""
    parts: list[str] = []

    if profile.get("name"):
        parts.append(f"Name: {profile['name']}")
    if profile.get("headline"):
        parts.append(f"Headline: {profile['headline']}")

    summary = profile.get("profile_summary")
    if summary:
        text = summary.get("summary") if isinstance(summary, dict) else summary
        if text:
            parts.append(f"Summary: {text}")

    skills = profile.get("skills_graph") or profile.get("skills") or []
    if skills:
        names = []
        for s in skills:
            if isinstance(s, dict) and s.get("name"):
                names.append(str(s["name"]))
            elif isinstance(s, str):
                names.append(s)
        if names:
            parts.append(f"Skills: {', '.join(names)}")

    role_parts = []
    for key in ("current_role", "current_company", "location"):
        if profile.get(key):
            role_parts.append(str(profile[key]))
    if role_parts:
        parts.append("Position: " + ", ".join(role_parts))

    for project in profile.get("projects", []) or []:
        techs = ", ".join(project.get("technologies", []) or [])
        parts.append(
            f"Project: {project.get('title') or ''} — {project.get('description') or ''}"
            f" Technologies: {techs}"
        )

    for entry in profile.get("work_history", []) or []:
        parts.append(
            f"Work: {entry.get('title')} at {entry.get('company', '')} — "
            f"{entry.get('description') or ''}"
        )

    return "\n".join(p for p in parts if p)


def build_job_embedding_text(job: dict[str, Any]) -> str:
    """Turn a job posting into optimized text for embeddings."""
    combine: list[str] = []
    if job.get("title"):
        combine.append(f"Job Title: {job['title']}")
    if job.get("description"):
        combine.append(f"Description: {job['description']}")
    if job.get("required_skills"):
        combine.append(f"Required Skills: {', '.join(job['required_skills'])}")
    if job.get("preferred_skills"):
        combine.append(f"Preferred Skills: {', '.join(job['preferred_skills'])}")
    if job.get("responsibilities"):
        combine.append(f"Responsibilities: {', '.join(job['responsibilities'])}")
    if job.get("location"):
        combine.append(f"Location: {job['location']}")
    if job.get("work_mode"):
        combine.append(f"Work Mode: {job['work_mode']}")

    return "\n".join(combine)


class EmbeddingService:
    """Generates and stores embeddings for candidates and jobs."""

    def __init__(self, qdrant: QdrantService | None = None) -> None:
        self._client = get_gemini_client()
        self._qdrant = qdrant or QdrantService()

    async def embed_candidate(
        self,
        candidate_id: str,
        profile: dict[str, Any],
        collection_name: str | None = None,
    ) -> str:
        """Generate and store a candidate's profile embedding. Returns point ID."""
        collection = collection_name or settings.qdrant_collection_candidates
        text = build_candidate_embedding_text(profile)
        vector = await self._client.generate_embedding(text)
        self._qdrant.ensure_collection(collection)

        point_id = f"candidate_{candidate_id}"
        self._qdrant.upsert_vector(
            collection_name=collection,
            point_id=point_id,
            vector=vector,
            payload=self._candidate_payload(profile),
        )
        return point_id

    async def embed_job(
        self,
        job_id: str,
        job_data: dict[str, Any],
        collection_name: str | None = None,
    ) -> str:
        """Generate and store a job's embedding. Returns point ID."""
        collection = collection_name or settings.qdrant_collection_jobs
        text = build_job_embedding_text(job_data)
        vector = await self._client.generate_embedding(text)
        self._qdrant.ensure_collection(collection)

        point_id = f"job_{job_id}"
        self._qdrant.upsert_vector(
            collection_name=collection,
            point_id=point_id,
            vector=vector,
            payload={
                "job_id": job_id,
                "title": job_data.get("title"),
                "company_id": job_data.get("company_id"),
            },
        )
        return point_id

    async def remove(self, collection_name: str, point_id: str) -> None:
        """Remove an embedding from Qdrant."""
        self._qdrant.delete_vector(collection_name, point_id)

    def _candidate_payload(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Build the Qdrant payload for candidate filtering."""
        return {
            "candidate_id": profile.get("id"),
            "name": profile.get("name"),
            "headline": profile.get("headline"),
            "location": profile.get("location"),
            "years_of_experience": profile.get("years_of_experience"),
            "evidence_confidence": profile.get("evidence_confidence"),
        }
