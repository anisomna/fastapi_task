from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse as CategorySchema, Category
from fastapi import HTTPException, status
from core.exceptions.database_exceptions import CategorySlugAlreadyExistsException
from core.exceptions.domain_exceptions import CategorySlugIsNotUniqueException
import logging

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: Category) -> CategorySchema:
        with self._database.session() as session:
            try:
                category = self._repo.create_category(session=session, data=data)
            except CategorySlugAlreadyExistsException:
                error = CategorySlugIsNotUniqueException(slug=data.slug)
                logger.error(error.get_detail())
                raise error

            return CategorySchema.model_validate(obj=category)
