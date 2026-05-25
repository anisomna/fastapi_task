from typing import List
from application.schemas.posts import PostImageResponse
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException
import logging

logger = logging.getLogger(__name__)


class GetPostImagesUseCase:
    def __init__(self) -> None:
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> List[PostImageResponse]:
        async with database.session() as session:
            try:
                post = await self._repo.get_post_by_id(session, post_id)
                images = await self._repo.get_post_images(session, post_id)
            except Exception:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            
            return [PostImageResponse(post_id=post_id, image=img) for img in images]
