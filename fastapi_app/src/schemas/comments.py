from pydantic import BaseModel, Field
from datetime import datetime


class Comment(BaseModel):
    id: int
    text: str = Field(..., description='Текст комментария')
    created_at: datetime = Field(description='Добавлено')
    post_id: int = Field(description='Публикация')
    author_id: int = Field(description='Автор комментария')
