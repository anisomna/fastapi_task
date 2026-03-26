from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentResponse as CommentSchema
from core.exceptions.database_exceptions import CommentNotFoundException
from core.exceptions.domain_exceptions import CommentNotFoundByIdException
import logging

logger = logging.getLogger(__name__)


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentSchema:
        with self._database.session() as session:
            try:
                comment = self._repo.get_comment_by_id(session, comment_id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error

            return CommentSchema.model_validate(obj=comment)
