from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.core.exceptions.database_exceptions import CommentNotFoundException
from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException
import logging

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete_comment(session=session, comment_id=comment_id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error
