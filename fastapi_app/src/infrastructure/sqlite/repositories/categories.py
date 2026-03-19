from typing import Type, List
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.categories import Category
from datetime import datetime

class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_all_categories(self, session: Session) -> List[Category]:
        query = session.query(self._model).order_by(self._model.title)
        return query.all()

    def get_category_by_id(self, session: Session, category_id: int) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == category_id)
        )
        return query.scalar()

    def get_category_by_slug(self, session: Session, slug: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        return query.scalar()

    def get_published_categories(self, session: Session) -> List[Category]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True)
        )
        return query.all()

    def get_category_by_slug(self, session: Session, slug: str) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        return query.scalar()

    def create_category(self, session: Session, title: str, description: str,
        slug: str, is_published: bool = True) -> Category:
        category = self._model(
            title=title,
            description=description,
            slug=slug,
            is_published=is_published,
            created_at=datetime.now()
        )
        session.add(category)
        session.flush()
        return category

    def delete_category(self, session: Session, category_id: int) -> bool:
        category = self.get_category_by_id(session, category_id)

        if category:
            session.delete(category)
            return True
        return False
