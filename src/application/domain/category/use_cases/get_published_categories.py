from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import CategoryResponse as CategorySchema
from typing import List


class GetPublishedCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[CategorySchema]:
        with self._database.session() as session:
            categories = self._repo.get_published_categories(session)

            result = []
            for category in categories:
                result.append(CategorySchema.model_validate(obj=category))

            return result
