from infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from .posts import Post


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    posts: Mapped["Post"] = relationship(back_populates="location")
