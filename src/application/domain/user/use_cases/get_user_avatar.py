from fastapi.responses import FileResponse
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.core.exceptions.domain_exceptions import UserNotFoundByIdException, UserHasNoImageException
from application.core.exceptions.database_exceptions import UserNotFoundException
import os
import logging

logger = logging.getLogger(__name__)


class GetUserAvatarUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()
        self.image_folder = "/fastapi_app/avatars"

    async def execute(self, user_id: int) -> FileResponse:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_user_by_id(session, user_id)
        except UserNotFoundException:
            error = UserNotFoundByIdException(id=user_id)
            logger.error(error.get_detail())
            raise error

        if not user.image:
            error = UserHasNoImageException()
            logger.error(error.get_detail())
            raise error

        full_image_path = f"{self.image_folder}/{user.image}"
        
        if not os.path.exists(full_image_path):
            error = UserHasNoImageException()
            logger.error(error.get_detail())
            raise error
        
        media_type = "image/jpeg"
        if user.image.lower().endswith('.png'):
            media_type = "image/png"
        elif user.image.lower().endswith('.gif'):
            media_type = "image/gif"
        elif user.image.lower().endswith('.jpg') or user.image.lower().endswith('.jpeg'):
            media_type = "image/jpeg"
            
        return FileResponse(full_image_path, media_type=media_type)
