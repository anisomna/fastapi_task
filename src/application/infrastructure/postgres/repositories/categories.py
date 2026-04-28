from typing import Type, List
from sqlalchemy import insert, select
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
        query = session.query(self._model).order_by(self._model.title)
        categories = query.all()

        if not categories:
            raise CategoryNotFoundException()

        return categories

    async def get_category_by_id(self, session: AsyncSession, category_id: int) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == category_id)
        )
        category = query.scalar()

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_category_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        category = query.scalar()

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_published_categories(self, session: AsyncSession) -> List[Category]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True)
        )
        categories = query.all()

        if not categories:
            raise CategoryNotFoundException()

        return categories

    async def create_category(self, session: AsyncSession, data: CategorySchema) -> Category:
        existing_category = session.scalar(
            select(self._model).where(self._model.slug == data.slug)
        )
        if existing_category is not None:
            raise CategorySlugAlreadyExistsException()
            
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        category = session.scalar(query)

        return category

    async def delete_category(self, session: AsyncSession, category_id: int) -> None:
        category = self.get_category_by_id(session, category_id)

        if category:
            session.delete(category)
        else:
            raise CategoryNotFoundException()
