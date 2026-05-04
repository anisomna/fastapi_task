from uuid import uuid4
import shutil
from fastapi import UploadFile
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.posts import PostImageResponse
from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
    PostNotFoundByIdException
)
import logging

logger = logging.getLogger(__name__)


class AddPostImageUseCase:
    def __init__(self) -> None:
        self.image_folder = "/fastapi_app/images"
        self._repo = PostRepository()

    async def execute(self, post_id: int, image: UploadFile) -> PostImageResponse:
        async with database.session() as session:
            try:
                post = await self._repo.get_post_by_id(session=session, post_id=post_id)
            except Exception:
                raise PostNotFoundByIdException(id=post_id)
            
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

            updated_post = await self._repo.update_post_image(
                session=session, 
                post_id=post_id, 
                image_path=new_image_filename
            )
            
            await session.commit()
            
            return PostImageResponse(post_id=post_id, image=new_image_filename)