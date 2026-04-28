from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Comment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    created_at: datetime = Field(description='Добавлено')
    post_id: int = Field(description='Публикация')
    author_id: int = Field(description='Автор комментария')


class CommentResponse(Comment):
    id: int

    model_config = ConfigDict(from_attributes=True)
