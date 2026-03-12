from infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    login: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )
    last_name: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
