from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import CategoryRepository
from application.schemas.categories import CategoryResponse as CategorySchema
from typing import List


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[CategorySchema]:
        async with self._database.session() as session:
            categories = await self._repo.get_all_categories(session)

            result = []
            for category in categories:
                result.append(CategorySchema.model_validate(obj=category))

            return result
