from pydantic import BaseModel, Field
from datetime import datetime


class Location(BaseModel):
    name: str = Field(..., description='Название места', max_length=256)
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Добавлено')
