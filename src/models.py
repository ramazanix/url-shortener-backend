from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, DateTime, func
from src.db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import uuid4, UUID


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    urls: Mapped[List["Url"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, created_at={self.created_at!r})"


class Url(Base):
    __tablename__ = "urls"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    short_name: Mapped[str] = mapped_column(index=True, unique=True)
    full_name: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="urls")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    def __repr__(self) -> str:
        return f"Url(id={self.id!r}, short_name={self.short_name!r}, full_name={self.full_name!r}, user_id={self.user_id!r})"
