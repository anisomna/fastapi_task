from uuid import uuid4
import shutil
from pathlib import Path
from fastapi import UploadFile
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import CommentRepository
from application.schemas.comments import CommentImageResponse
from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
    CommentNotFoundByIdException,
)
import logging

logger = logging.getLogger(__name__)


class AddCommentImageUseCase:
    def __init__(self) -> None:
        self.image_folder = Path("/fastapi_app/comment_images")
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, image: UploadFile) -> CommentImageResponse:
        async with database.session() as session:
            try:
                comment = await self._repo.get_comment_by_id(session, comment_id)
            except Exception:
                raise CommentNotFoundByIdException(id=comment_id)
            if not image.filename:
                raise UploadFileIsNotImageException()
            
            file_extension = image.filename.split(".")[-1].lower()
            if file_extension not in ["jpeg", "jpg", "png", "gif"]:
                raise UploadFileIsNotImageException()
            
            self.image_folder.mkdir(parents=True, exist_ok=True)
            new_image_name = str(uuid4())
            new_image_filename = f"{new_image_name}.{file_extension}"
            new_image_path = self.image_folder / new_image_filename
            
            with open(new_image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            await self._repo.add_comment_images(
                session=session,
                comment_id=comment_id,
                image_paths=[new_image_filename]  
            )
            await session.commit()

            return CommentImageResponse(comment_id=comment_id, image=new_image_filename)
