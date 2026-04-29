from typing import List
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.posts import PostResponse as PostSchema


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> List[PostSchema]:
        async with self._database.session() as session:
            posts = await self._repo.get_all_posts(session)

            result = []
            for post in posts:
                result.append(PostSchema.model_validate(obj=post))

            return result
