from typing import List
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import CommentResponse as CommentSchema


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> List[CommentSchema]:
        with self._database.session() as session:
            comments = self._repo.get_all_comments(session)

            result = []
            for comment in comments:
                result.append(CommentSchema.model_validate(obj=comment))

            return result
