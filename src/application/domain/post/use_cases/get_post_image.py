from fastapi.responses import FileResponse
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException, PostHasNoImageException
from application.core.exceptions.database_exceptions import PostNotFoundException
import logging

logger = logging.getLogger(__name__)


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self.image_folder = "./../images"

    async def execute(self, post_id: int) -> FileResponse:
        try:
            async with self._database.session() as session:
                post = await self._repo.get_post_by_id(session, post_id)
        except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error

        if not post.image_path:
            error = PostHasNoImageException()
            logger.error(error.get_detail())
            raise error

        full_image_path: str = f"{self.image_folder}/{post.image_path}.jpeg"
        return FileResponse(full_image_path, media_type="image/jpeg")
