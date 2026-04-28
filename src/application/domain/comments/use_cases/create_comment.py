from datetime import datetime
from fastapi import HTTPException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import CommentResponse as CommentSchema, Comment
from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException
)
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException
)
import logging

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, data: Comment) -> CommentSchema:
        with self._database.session() as session:
            try:
                comment = self._repo.create_comment(session=session, data=data)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=data.post_id)
                logger.error(error.get_detail())
                raise error
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=data.author_id)
                logger.error(error.get_detail())
                raise error

            return CommentSchema.model_validate(obj=comment)
