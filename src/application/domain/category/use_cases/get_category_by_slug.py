from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import CategoryResponse as CategorySchema
from application.core.exceptions.database_exceptions import CategoryNotFoundException
from application.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException
import logging

logger = logging.getLogger(__name__)


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: int) -> CategorySchema:
        with self._database.session() as session:
            try:
                category = self._repo.get_category_by_slug(session, slug)
            except CategoryNotFoundException:
                error = CategoryNotFoundBySlugException(slug=slug)
                logger.error(error.get_detail())
                raise error

            return CategorySchema.model_validate(obj=category)
