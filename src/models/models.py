from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.mixins import SoftDeleteMixin, TimestampMixin


class Base(DeclarativeBase):
    __abstract__ = True  # parametro para indicar que es una clase abstracta

    @classmethod
    def all_active(cls, session):
        """Query personalizado para obtener solo elementos no eliminados. (soft delete)"""
        return session.query(cls).filter(cls.deleted_at.is_(None))

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(cls).filter(cls.id == id, cls.deleted_at.is_(None)).first()


class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(30), nullable=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.fullname!r}, email={self.email!r})"


class Post(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(5000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, user_id={self.user_id!r})"


class Comment(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"Comment(id={self.id!r}, content={self.content!r}, post_id={self.post_id!r})"
