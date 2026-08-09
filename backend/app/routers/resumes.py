"""Resumes router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_candidate, get_current_user, get_db
from app.schemas.resume import ResumeResponse, ResumeUploadResponse
from app.services.resume import ResumeService

router = APIRouter(tags=["resumes"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    candidate_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Upload a resume for AI analysis."""
    service = ResumeService(db)
    file_data = await file.read()
    content_type = file.content_type or "application/pdf"
    resume = await service.upload_resume(
        candidate_id=candidate_id,
        file_data=file_data,
        file_name=file.filename or "resume.pdf",
        file_type=content_type,
    )
    return ResumeUploadResponse(
        id=resume.id,
        file_url=resume.file_url,
        processing_status=resume.processing_status,
    )


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all resumes for a candidate."""
    service = ResumeService(db)
    return await service.list_resumes(candidate_id)


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get resume by ID."""
    service = ResumeService(db)
    return await service.get_resume(resume_id)
