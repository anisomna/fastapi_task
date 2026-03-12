from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import Comment as CommentSchema


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentSchema:
        with self._database.session() as session:
            comment = self._repo.get_by_id(session, comment_id)

            if not comment:
                raise ValueError("Не удалось найти комментарий")

            comment_dict = {
                "id": comment.id,
                "text": comment.text,
                "created_at": comment.created_at,
                "post_id": comment.post_id,
                "author_id": comment.author_id
            }

            return CommentSchema.model_validate(obj=comment_dict)
