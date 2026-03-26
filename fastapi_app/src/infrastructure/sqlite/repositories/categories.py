from typing import Type, List
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.categories import Category
from datetime import datetime
from schemas.categories import Category as CategorySchema
from core.exceptions.database_exceptions import CategoryNotFoundException


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_all_categories(self, session: Session) -> List[Category]:
        query = session.query(self._model).order_by(self._model.title)
        categories = query.all()

        if not categories:
            raise CategoryNotFoundException()

        return categories

    def get_category_by_id(self, session: Session, category_id: int) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == category_id)
        )
        category = query.scalar()

        if not category:
            raise CategoryNotFoundException()

        return category

    def get_category_by_slug(self, session: Session, slug: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        category = query.scalar()

        if not category:
            raise CategoryNotFoundException()

        return category

    def get_published_categories(self, session: Session) -> List[Category]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True)
        )
        categories = query.all()

        if not categories:
            raise CategoryNotFoundException()

        return categories

    def create_category(self, session: Session, data: CategorySchema) -> Category:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        category = session.scalar(query)

        return category

    def delete_category(self, session: Session, category_id: int) -> None:
        category = self.get_category_by_id(session, category_id)

        if category:
            session.delete(category)
        else:
            raise CategoryNotFoundException()
