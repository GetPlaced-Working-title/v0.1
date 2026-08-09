"""Certificates router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_candidate, get_current_user, get_db
from app.core.storage import StorageService
from app.core.exceptions import NotFoundError
from app.schemas.certificate import CertificateCreate, CertificateResponse
from app.repositories.base import BaseRepository
from app.models.certificate import Certificate

router = APIRouter(tags=["certificates"])


@router.post("", response_model=CertificateResponse)
async def add_certificate(
    candidate_id: str,
    data: CertificateCreate,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Add a certificate manually."""
    repo = BaseRepository(Certificate, db)
    return await repo.create(
        candidate_id=candidate_id,
        source="manual",
        processing_status="pending",
        **data.model_dump(),
    )


@router.post("/upload", response_model=CertificateResponse)
async def upload_certificate(
    candidate_id: str,
    file: UploadFile = File(...),
    name: str = "",
    issuer: str | None = None,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Upload a certificate file."""
    storage = StorageService()
    file_data = await file.read()
    key = StorageService.generate_key("certificates", file.filename or "cert.pdf", candidate_id)
    storage.upload_file(file_data, key, content_type=file.content_type or "application/pdf")

    repo = BaseRepository(Certificate, db)
    return await repo.create(
        candidate_id=candidate_id,
        name=name or file.filename,
        issuer=issuer,
        file_url=storage.get_file_url(key),
        source="upload",
        processing_status="pending",
    )


@router.get("", response_model=list[CertificateResponse])
async def list_certificates(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List certificates for a candidate."""
    repo = BaseRepository(Certificate, db)
    return await repo.get_all(filters={"candidate_id": candidate_id})


@router.get("/{certificate_id}", response_model=CertificateResponse)
async def get_certificate(
    certificate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get certificate by ID."""
    repo = BaseRepository(Certificate, db)
    cert = await repo.get_by_id(certificate_id)
    if not cert:
        raise NotFoundError("Certificate not found")
    return cert
