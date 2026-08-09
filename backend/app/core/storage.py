"""Cloudflare R2 storage client (S3-compatible)."""

from __future__ import annotations

import hashlib
from io import BytesIO
from typing import Any, BinaryIO

import boto3
from botocore.config import Config as BotoConfig

from app.core.config import get_settings

settings = get_settings()

_s3_client: Any = None


def get_s3_client() -> Any:
    """Get or create the S3 client for R2."""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=settings.r2_endpoint_url,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            config=BotoConfig(
                signature_version="s3v4",
                retries={"max_attempts": 3, "mode": "adaptive"},
            ),
            region_name="auto",
        )
    return _s3_client


class StorageService:
    """File storage operations using Cloudflare R2."""

    def __init__(self, client: Any | None = None) -> None:
        self._client = client or get_s3_client()
        self._bucket = settings.r2_bucket_name
        self._public_url = settings.r2_public_url

    def upload_file(
        self,
        file_data: BinaryIO | bytes,
        key: str,
        content_type: str = "application/octet-stream",
        metadata: dict[str, str] | None = None,
    ) -> str:
        """Upload a file and return the storage key."""
        if isinstance(file_data, bytes):
            file_data = BytesIO(file_data)

        extra_args: dict[str, Any] = {"ContentType": content_type}
        if metadata:
            extra_args["Metadata"] = metadata

        self._client.upload_fileobj(
            file_data,
            self._bucket,
            key,
            ExtraArgs=extra_args,
        )
        return key

    def get_file_url(self, key: str) -> str:
        """Get the public URL for a file."""
        if self._public_url:
            return f"{self._public_url.rstrip('/')}/{key}"
        return f"{settings.r2_endpoint_url}/{self._bucket}/{key}"

    def generate_presigned_url(
        self,
        key: str,
        expiration: int = 3600,
        method: str = "get_object",
    ) -> str:
        """Generate a pre-signed URL for temporary access."""
        return self._client.generate_presigned_url(
            method,
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expiration,
        )

    def delete_file(self, key: str) -> None:
        """Delete a file."""
        self._client.delete_object(Bucket=self._bucket, Key=key)

    def file_exists(self, key: str) -> bool:
        """Check if a file exists."""
        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except Exception:
            return False

    def get_file(self, key: str) -> bytes:
        """Download a file's contents."""
        response = self._client.get_object(Bucket=self._bucket, Key=key)
        return response["Body"].read()

    @staticmethod
    def generate_key(
        folder: str,
        filename: str,
        candidate_id: str,
    ) -> str:
        """Generate a storage key: folder/candidate_id/hash_filename."""
        file_hash = hashlib.md5(filename.encode()).hexdigest()[:8]
        extension = filename.rsplit(".", 1)[-1] if "." in filename else ""
        return f"{folder}/{candidate_id}/{file_hash}.{extension}"
