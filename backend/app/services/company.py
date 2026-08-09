"""Company service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.company import Company
from app.repositories.company import CompanyRepository


class CompanyService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CompanyRepository(session)

    async def create_company(self, user_id: str, **kwargs) -> Company:
        existing = await self.repo.get_by_user_id(user_id)
        if existing:
            raise ConflictError("Company already exists for this user")
        return await self.repo.create(user_id=user_id, **kwargs)

    async def get_company(self, company_id: str) -> Company:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundError("Company not found")
        return company

    async def get_by_user_id(self, user_id: str) -> Company | None:
        return await self.repo.get_by_user_id(user_id)

    async def update_company(self, company_id: str, **kwargs) -> Company:
        company = await self.get_company(company_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(company, key, value)
        return company

    async def list_companies(self, offset: int = 0, limit: int = 20):
        items = await self.repo.get_all(offset=offset, limit=limit)
        total = await self.repo.count()
        return list(items), total
