"""Videos router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_candidate, get_current_user, get_db
from app.core.exceptions import NotFoundError
from app.core.storage import StorageService
from app.models.video import Video
from app.repositories.base import BaseRepository
from app.schemas.video import VideoResponse, VideoUploadResponse

router = APIRouter(tags=["videos"])


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(
    candidate_id: str,
    file: UploadFile = File(...),
    title: str | None = None,
    current_user: dict = Depends(get_current_candidate),
    db: AsyncSession = Depends(get_db),
):
    """Upload a skill demonstration video."""
    storage = StorageService()
    file_data = await file.read()
    key = StorageService.generate_key("videos", file.filename or "video.mp4", candidate_id)
    storage.upload_file(file_data, key, content_type=file.content_type or "video/mp4")

    repo = BaseRepository(Video, db)
    video = await repo.create(
        candidate_id=candidate_id,
        title=title or file.filename,
        file_url=storage.get_file_url(key),
        file_size=len(file_data),
        processing_status="pending",
    )
    return VideoUploadResponse(
        id=video.id,
        file_url=video.file_url,
        processing_status="pending",
    )


@router.get("", response_model=list[VideoResponse])
async def list_videos(
    candidate_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List videos for a candidate."""
    repo = BaseRepository(Video, db)
    items = await repo.get_all(filters={"candidate_id": candidate_id})
    return items


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get video by ID."""
    repo = BaseRepository(Video, db)
    video = await repo.get_by_id(video_id)
    if not video:
        raise NotFoundError("Video not found")
    return video
