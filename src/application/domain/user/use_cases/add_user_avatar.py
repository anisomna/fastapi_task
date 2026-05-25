from uuid import uuid4
import shutil
from fastapi import UploadFile
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserImageResponse
from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
    UserNotFoundByIdException
)
import logging

logger = logging.getLogger(__name__)


class AddUserAvatarUseCase:
    def __init__(self) -> None:
        self.image_folder = "/fastapi_app/avatars"
        self._repo = UserRepository()

    async def execute(self, user_id: int, image: UploadFile) -> UserImageResponse:
        async with database.session() as session:
            try:
                user = await self._repo.get_user_by_id(session=session, user_id=user_id)
            except Exception:
                raise UserNotFoundByIdException(id=user_id)
            
            file_extension = image.filename.split(".")[-1].lower()
            if file_extension not in ["jpeg", "jpg", "png", "gif"]:
                error = UploadFileIsNotImageException()
                logger.error(error.get_detail())
                raise error

            new_image_name: str = str(uuid4())
            new_image_filename: str = f"{new_image_name}.{file_extension}"
            new_image_path: str = f"{self.image_folder}/{new_image_filename}"

            with open(new_image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            updated_user = await self._repo.update_user_avatar(
                session=session, 
                user_id=user_id, 
                image_path=new_image_filename
            )
            
            await session.commit()
            
            return UserImageResponse(user_id=user_id, image=new_image_filename)
