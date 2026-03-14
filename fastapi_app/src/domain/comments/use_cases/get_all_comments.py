from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import Comment as CommentSchema


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> List[CommentSchema]:
        with self._database.session() as session:
            comments = self._repo.get_all_comments(session)

            result = []
            for comment in comments:
                comment_dict = {
                    "id": comment.id,
                    "text": comment.text,
                    "created_at": comment.created_at,
                    "post_id": comment.post_id,
                    "author_id": comment.author_id
                }

                result.append(CommentSchema.model_validate(obj=comment_dict))

            return result
