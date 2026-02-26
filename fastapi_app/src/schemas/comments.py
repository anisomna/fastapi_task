from pydantic import BaseModel, Field
from datetime import datetime
from schemas.posts import Post
from schemas.users import User


class Comment(BaseModel):
    text: str = Field(..., description='Текст комментария')
    created_at: datetime = Field(description='Добавлено')
    post: Post = Field(description='Публикация')
    author: User = Field(description='Автор комментария')
