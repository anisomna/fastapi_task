from datetime import datetime
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.comments import Comment as CommentSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()

    async def execute(self, text: str, post_id: int, author_id: int) -> CommentSchema:
        with self._database.session() as session:
            author = self._user_repo.get_user_by_id(session, author_id)

            if not author:
                raise ValueError("Автор не найден")

            comment = self._repo.create_comment(
                session=session,
                text=text,
                post_id=post_id,
                author_id=author_id
            )

            comment_dict = {
                "id": comment.id,
                "text": comment.text,
                "created_at": comment.created_at,
                "post_id": comment.post_id,
                "author_id": comment.author_id
            }

            return CommentSchema.model_validate(obj=comment_dict)
