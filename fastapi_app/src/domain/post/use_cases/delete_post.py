from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> bool:
        with self._database.session() as session:
            post = self._repo.get_post_by_id(session, post_id)

            if not post:
                raise ValueError(f"Публикация с id {post_id} не найдена")

            result = self._repo.delete_post(session, post_id)
            return result
