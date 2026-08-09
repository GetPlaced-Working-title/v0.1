"""GitHub analyzer."""

from __future__ import annotations

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.analyzers.base import BaseAnalyzer
from app.ai.prompts.github import GITHUB_ANALYSIS_PROMPT
from app.core.logging import get_logger

logger = get_logger(__name__)

GITHUB_API_URL = "https://api.github.com"


class GitHubService:
    """Fetches GitHub data via the GitHub API."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token

    async def fetch_profile(self, username: str) -> dict:
        """Fetch a user's GitHub profile."""
        async with httpx.AsyncClient(timeout=30) as client:
            headers = self._headers()
            response = await client.get(
                f"{GITHUB_API_URL}/users/{username}",
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "username": data.get("login"),
                "profile_url": data.get("html_url"),
                "created_at": data.get("created_at"),
                "public_repos": data.get("public_repos", 0),
                "followers": data.get("followers", 0),
                "following": data.get("following", 0),
            }

    async def fetch_repositories(self, username: str, limit: int = 30) -> list[dict]:
        """Fetch a user's most recent repositories."""
        async with httpx.AsyncClient(timeout=30) as client:
            headers = self._headers()
            response = await client.get(
                f"{GITHUB_API_URL}/users/{username}/repos",
                params={
                    "sort": "pushed",
                    "direction": "desc",
                    "per_page": limit,
                },
                headers=headers,
            )
            response.raise_for_status()
            repos = response.json()
            return [
                {
                    "name": r.get("name"),
                    "description": r.get("description"),
                    "language": r.get("language"),
                    "stargazers_count": r.get("stargazers_count", 0),
                    "forks_count": r.get("forks_count", 0),
                    "watchers_count": r.get("watchers_count", 0),
                    "created_at": r.get("created_at"),
                    "updated_at": r.get("updated_at"),
                    "pushed_at": r.get("pushed_at"),
                    "fork": r.get("fork", False),
                    "homepage": r.get("homepage"),
                    "topics": r.get("topics", []),
                    "size": r.get("size", 0),
                    "open_issues_count": r.get("open_issues_count", 0),
                }
                for r in repos
            ]

    async def fetch_readme(self, owner: str, repo: str) -> str | None:
        """Fetch a repository's README content."""
        async with httpx.AsyncClient(timeout=30) as client:
            headers = self._headers()
            headers["Accept"] = "application/vnd.github.raw+json"
            response = await client.get(
                f"{GITHUB_API_URL}/repos/{owner}/{repo}/readme",
                headers=headers,
            )
            if response.status_code == 404:
                return None
            if response.status_code == 200:
                return response.text[:20000]
            return None

    def _headers(self) -> dict[str, str]:
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}


class GitHubAnalyzer(BaseAnalyzer):
    """Fetches GitHub data and analyzes engineering quality."""

    analyzer_type = "github_analysis"

    def __init__(self, client=None, github_token: str | None = None) -> None:
        super().__init__(client)
        self.github = GitHubService(token=github_token)

    async def fetch_and_analyze(
        self,
        username: str,
        session: AsyncSession | None = None,
    ) -> dict:
        """Fetch GitHub profile + repos, then analyze them together."""
        try:
            profile = await self.github.fetch_profile(username)
            repos = await self.github.fetch_repositories(username)

            # Build content for AI analysis
            content = self._build_content(profile, repos)
            analysis = await self.analyze(content, session)

            analysis["profile_data"] = profile
            analysis["repository_data"] = repos
            return analysis
        except httpx.HTTPError as e:
            logger.error("github_fetch_error", username=username, error=str(e))
            raise

    def _build_content(self, profile: dict, repos: list[dict]) -> str:
        """Build the analysis content from fetched GitHub data."""
        lines = [f"GitHub username: {profile.get('username')}"]
        lines.append(
            f"Account created: {profile.get('created_at', 'unknown')}, "
            f"public repos: {profile.get('public_repos', 0)}, "
            f"followers: {profile.get('followers', 0)}"
        )

        lines.append("\n## Repositories:")
        for repo in repos:
            lines.append(
                f"- {repo.get('name')}: {repo.get('description') or 'no description'}\n"
                f"  Language: {repo.get('language') or 'unknown'}, "
                f"Stars: {repo.get('stargazers_count', 0)}, "
                f"Forks: {repo.get('forks_count', 0)}, "
                f"Fork: {repo.get('fork', False)}, "
                f"Topics: {', '.join(repo.get('topics', []) or [])}, "
                f"Last pushed: {repo.get('pushed_at')}, "
                f"Homepage: {repo.get('homepage') or 'none'}"
            )

        return "\n".join(lines)

    async def analyze(
        self,
        content: str,
        session: AsyncSession | None = None,
    ) -> dict:
        """Analyze fetched GitHub data."""
        return await self._run_with_cache(
            content=content,
            session=session,
            prompt_template=GITHUB_ANALYSIS_PROMPT,
        )
