from typing import Type, List
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.categories import Category


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_all_categories(self, session: Session) -> List[Category]:
        query = session.query(self._model).order_by(self._model.name)
        return query.all()

    def get_category_by_id(self, session: Session, category_id: int) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == category_id)
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
