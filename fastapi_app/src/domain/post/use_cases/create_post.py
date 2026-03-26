from datetime import datetime
from fastapi import HTTPException
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponse as PostSchema, Post
from core.exceptions.database_exceptions import (
    UserNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException
)
from core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException
)
import logging

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: Post) -> PostSchema:
        with self._database.session() as session:
            try:
                post = self._repo.create_post(session=session, data=data)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=data.author_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundException:
                if data.category_id is not None:
                    error = CategoryNotFoundByIdException(id=data.category_id)
                    logger.error(error.get_detail())
                    raise error
                error = CategoryNotFoundException()
                logger.error(error.get_detail())
                raise error
            except LocationNotFoundException:
                if data.location_id is not None:
                    error = LocationNotFoundByIdException(id=data.location_id)
                    logger.error(error.get_detail())
                    raise error
                error = LocationNotFoundException()
                logger.error(error.get_detail())
                raise error

            return PostSchema.model_validate(obj=post)
