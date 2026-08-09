"""Celery tasks for certificate analysis."""

from __future__ import annotations

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.certificate.analyze_certificate")
def analyze_certificate(certificate_id: str) -> dict:
    """Analyze and verify a certificate."""
    import asyncio
    return asyncio.run(_analyze_certificate_async(certificate_id))


async def _analyze_certificate_async(certificate_id: str) -> dict:
    from app.core.database import async_session_factory
    from app.ai.analyzers.certificate import CertificateAnalyzer
    from app.repositories.base import BaseRepository
    from app.models.certificate import Certificate

    async with async_session_factory() as session:
        repo = BaseRepository(Certificate, session)
        cert = await repo.get_by_id(certificate_id)
        if not cert:
            return {"error": "Certificate not found"}

        try:
            cert.processing_status = "processing"
            await session.commit()

            analyzer = CertificateAnalyzer()
            content = f"Certificate: {cert.name}, Issuer: {cert.issuer or 'unknown'}"
            if cert.credential_url:
                content += f", URL: {cert.credential_url}"

            analysis = await analyzer.analyze(content, session)

            cert.analysis = analysis
            cert.scores = analysis.get("scores", {})
            cert.is_verified = analysis.get("is_verified", False)

            from datetime import datetime, timezone
            cert.analyzed_at = datetime.now(timezone.utc)
            cert.processing_status = "completed"
            await session.commit()

            return {"status": "completed", "certificate_id": certificate_id}

        except Exception as e:
            cert.processing_status = "failed"
            cert.processing_error = str(e)
            await session.commit()
            return {"status": "failed", "error": str(e)}
