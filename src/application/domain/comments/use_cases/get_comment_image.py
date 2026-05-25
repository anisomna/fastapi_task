from typing import List
from application.schemas.comments import CommentImageResponse
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException
import logging

logger = logging.getLogger(__name__)


class GetCommentImagesUseCase:
    def __init__(self) -> None:
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> List[CommentImageResponse]:
        async with database.session() as session:
            try:
                comment = await self._repo.get_comment_by_id(session, comment_id)
                images = await self._repo.get_comment_images(session, comment_id)
            except Exception:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error

            return [CommentImageResponse(comment_id=comment_id, image=img) for img in images]
