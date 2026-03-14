from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> bool:
        with self._database.session() as session:
            comment = self._repo.get_comment_by_id(session, comment_id)

            if not comment:
                raise ValueError("Не удалось найти комментарий")

            result = self._repo.delete_comment(session, comment_id)
            return result
