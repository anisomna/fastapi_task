from typing import Type, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.infrastructure.postgres.models.categories import Category
from datetime import datetime
from application.schemas.categories import Category as CategorySchema
from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException
)


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    async def get_all_categories(self, session: AsyncSession) -> List[Category]:
        query = select(self._model).order_by(self._model.title)
        result = await session.execute(query)
        categories = result.scalars().all()

        if not categories:
            raise CategoryNotFoundException()

        return categories

    async def get_category_by_id(self, session: AsyncSession, category_id: int) -> Category:
        query = select(self._model).where(self._model.id == category_id)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_category_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = select(self._model).where(self._model.slug == slug)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_published_categories(self, session: AsyncSession) -> List[Category]:
        query = select(self._model).where(self._model.is_published == True)
        result = await session.execute(query)
        categories = result.scalars().all()

        if not categories:
            raise CategoryNotFoundException()

        return categories

    async def create_category(self, session: AsyncSession, data: CategorySchema) -> Category:
        existing_query = select(self._model).where(self._model.slug == data.slug)
        existing_result = await session.execute(existing_query)
        existing_category = existing_result.scalar_one_or_none()
        
        if existing_category is not None:
            raise CategorySlugAlreadyExistsException()
        
        category_data = data.model_dump(exclude_none=True)
        category = self._model(**category_data)
        session.add(category)
        await session.flush()
        await session.refresh(category)

        return category

    async def delete_category(self, session: AsyncSession, category_id: int) -> None:
        category = await self.get_category_by_id(session, category_id)

        if category:
            await session.delete(category)
            await session.flush()
        else:
            raise CategoryNotFoundException()
