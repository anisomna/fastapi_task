from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class Comment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    created_at: datetime = Field(description='Добавлено')
    post_id: int = Field(description='Публикация')
    author_id: int = Field(description='Автор комментария')


class CommentResponse(Comment):
    id: int
    images: List[str] = Field(default_factory=list, description="Список изображений")
    model_config = ConfigDict(from_attributes=True)


class CommentImageResponse(BaseModel):
    image: str
