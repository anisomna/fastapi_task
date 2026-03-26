from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponse as PostSchema
from core.exceptions.database_exceptions import PostNotFoundException
from core.exceptions.domain_exceptions import PostNotFoundByIdException
import logging

logger = logging.getLogger(__name__)


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostSchema:
        with self._database.session() as session:
            try:
                post = self._repo.get_post_by_id(session, post_id)
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error

            return PostSchema.model_validate(obj=post)
