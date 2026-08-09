"""Gemini AI client with caching, retries, and structured output."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)


class GeminiClient:
    """Unified Gemini API client for all AI analysis tasks."""

    def __init__(self) -> None:
        self._text_model = genai.GenerativeModel(settings.gemini_model)
        self._video_model = genai.GenerativeModel(settings.gemini_video_model)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
    async def analyze_text(
        self,
        prompt: str,
        content: str,
        response_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send text content for analysis and return structured JSON."""
        full_prompt = self._build_prompt(prompt, content, response_schema)

        response = await self._text_model.generate_content_async(
            full_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1,
                max_output_tokens=8192,
            ),
        )

        return self._parse_response(response)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
    async def analyze_video(
        self,
        prompt: str,
        video_file: Any,
        response_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Analyze video content using Gemini Video model."""
        full_prompt = self._build_prompt(prompt, "", response_schema)

        response = await self._video_model.generate_content_async(
            [video_file, full_prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1,
                max_output_tokens=8192,
            ),
        )

        return self._parse_response(response)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector for text."""
        result = genai.embed_content(
            model=f"models/{settings.gemini_embedding_model}",
            content=text,
            task_type="retrieval_document",
        )
        return result["embedding"]

    async def generate_query_embedding(self, text: str) -> list[float]:
        """Generate embedding optimized for search queries."""
        result = genai.embed_content(
            model=f"models/{settings.gemini_embedding_model}",
            content=text,
            task_type="retrieval_query",
        )
        return result["embedding"]

    @staticmethod
    def compute_input_hash(content: str, analyzer_type: str) -> str:
        """Compute SHA256 hash of input for caching."""
        raw = f"{analyzer_type}:{content}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _build_prompt(
        self,
        prompt: str,
        content: str,
        response_schema: dict[str, Any] | None,
    ) -> str:
        """Build the full prompt with schema instructions."""
        parts = [prompt]

        if content:
            parts.append(f"\n\n--- CONTENT TO ANALYZE ---\n{content}\n--- END CONTENT ---")

        if response_schema:
            schema_str = json.dumps(response_schema, indent=2)
            parts.append(
                f"\n\nRespond with valid JSON matching this schema exactly:\n{schema_str}"
            )

        return "\n".join(parts)

    def _parse_response(self, response: Any) -> dict[str, Any]:
        """Parse Gemini response into a Python dict."""
        try:
            text = response.text.strip()
            # Strip markdown code fences if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error("gemini_parse_error", error=str(e), raw_text=response.text[:500])
            raise ValueError(f"Failed to parse Gemini response: {e}") from e


# Singleton
_gemini_client: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    """Get or create the Gemini client singleton."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
