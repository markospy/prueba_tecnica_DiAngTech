from typing import List, Literal

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.mixins import SoftDeleteMixin, TimestampMixin

JOINED_LOAD_RELATIONS = Literal[
    "tags",
    "comments",
    "user",
]


class Base(DeclarativeBase):
    pass


class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    avatar: Mapped[str] = mapped_column(String(200), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    tags: Mapped[List["Tag"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.fullname!r}, email={self.email!r})"


association_table = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Post(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(5000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    tags: Mapped[List["Tag"]] = relationship(secondary="post_tag", back_populates="posts")

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


class Tag(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tags")
    posts: Mapped[List["Post"]] = relationship(secondary="post_tag", back_populates="tags")

    def __repr__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r})"
