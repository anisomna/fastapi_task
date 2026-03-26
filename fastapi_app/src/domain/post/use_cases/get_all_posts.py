from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponse as PostSchema


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> List[PostSchema]:
        with self._database.session() as session:
            posts = self._repo.get_all_posts(session)

            result = []
            for post in posts:
                result.append(PostSchema.model_validate(obj=post))

            return result
