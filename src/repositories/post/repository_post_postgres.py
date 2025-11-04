from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.models import Post, Tag
from src.repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from src.repositories.repository_base import RepositoryBase
from src.schemas.post import PostIn, PostPut


class RepositoryPostPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self, page: int, size: int) -> tuple[List[Post], int]:
        skip = (page - 1) * size
        base_query = (
            select(Post).options(joinedload(Post.user), joinedload(Post.tags)).where(Post.deleted_at.is_(None))
        )

        # Count
        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self.session.scalar(count_query)

        # Posts
        query = base_query.offset(skip).limit(size).order_by(Post.created_at.desc())
        result = await self.session.execute(query)
        posts = result.unique().scalars().all()

        if not posts:
            raise RepositoryNotFoundException("Not found posts")

        return posts, total

    async def get_by_id(self, id: int) -> Optional[Post]:
        result = await self.session.execute(
            select(Post)
            .options(joinedload(Post.user), joinedload(Post.tags))
            .where(Post.id == id, Post.deleted_at.is_(None))
        )
        post = result.unique().scalar_one_or_none()
        if not post:
            raise RepositoryNotFoundException(entity_name="Post", id=id)
        return post

    async def get_by_user_id(self, user_id: int) -> Optional[List[Post]]:
        result = await self.session.execute(
            select(Post)
            .options(joinedload(Post.user), joinedload(Post.tags))
            .where(Post.user_id == user_id, Post.deleted_at.is_(None))
        )
        posts = result.unique().scalars().all()
        if not posts:
            raise RepositoryNotFoundException(message=f"No posts found for user {user_id}")
        return posts

    async def get_by_tag(self, tag: str) -> Optional[List[Post]]:
        result = await self.session.execute(
            select(Post)
            .options(joinedload(Post.user), joinedload(Post.tags))
            .where(Post.tags.any(Tag.name == tag), Post.deleted_at.is_(None))
        )
        posts = result.unique().scalars().all()
        if not posts:
            raise RepositoryNotFoundException(message=f"No posts found for tag {tag}")
        return posts

    async def create(self, schema: PostIn, user_id: int) -> Optional[Post]:
        tags = []
        if schema.tags:
            for tag_name in schema.tags:
                result = await self.session.execute(select(Tag).where(Tag.name == tag_name))
                tag = result.unique().scalar()
                if tag:
                    if tag.deleted_at is not None:
                        tag.deleted_at = None
                    tags.append(tag)
                else:
                    try:
                        tag = Tag(name=tag_name, user_id=user_id)
                        self.session.add(tag)
                        tags.append(tag)
                    except (
                        IntegrityError
                    ):  # Puede ocurrir que justo en ese instante otro proceso haya creado el tag(concurrency issue)
                        tags.append(tag)
        post = Post(**schema.model_dump(exclude={"tags"}), user_id=user_id, tags=tags)
        try:
            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post, attribute_names=["id", "created_at", "updated_at"])
            # Recargar con las relaciones
            result = await self.session.execute(
                select(Post).options(joinedload(Post.user), joinedload(Post.tags)).where(Post.id == post.id)
            )
            post = result.unique().scalar_one()
            return post
        except IntegrityError:
            await self.session.rollback()
            raise RepositoryAlreadyExistsException(entity_name="Post", name=post.title)

    async def update(self, id: int, schema: PostPut, user_id: int) -> Optional[Post]:
        result = await self.session.execute(
            select(Post)
            .options(joinedload(Post.user), joinedload(Post.tags))
            .where(Post.id == id, Post.deleted_at.is_(None), Post.user_id == user_id)
        )
        post = result.unique().scalar_one_or_none()
        if not post:
            raise RepositoryNotFoundException(f"Not found post with id {id} for the user with id {user_id}")
        update_post_data = schema.model_dump(exclude_unset=True, exclude={"tags"})

        # Actualizar campos simples
        for key, value in update_post_data.items():
            setattr(post, key, value)

        # Manejar tags si están presentes
        if schema.tags is not None:
            tags = []
            for tag_name in schema.tags:
                tag_result = await self.session.execute(select(Tag).where(Tag.name == tag_name))
                tag = tag_result.unique().scalar()
                if tag:
                    tags.append(tag)
                else:
                    try:
                        tag = Tag(name=tag_name, user_id=user_id)
                        self.session.add(tag)
                        tags.append(tag)
                    except (
                        IntegrityError
                    ):  # Puede ocurrir que justo en ese instante otro proceso haya creado el tag(concurrency issue)
                        tags.append(tag)
            post.tags = tags

        try:
            await self.session.commit()
            await self.session.refresh(post, attribute_names=["updated_at"])
            # Recargar con las relaciones
            result = await self.session.execute(
                select(Post).options(joinedload(Post.user), joinedload(Post.tags)).where(Post.id == post.id)
            )
            post = result.unique().scalar_one()
            return post
        except IntegrityError:
            await self.session.rollback()
            raise RepositoryAlreadyExistsException(entity_name="Post", name=post.title)

    async def delete(self, id: int, user_id: int) -> None:
        result = await self.session.execute(
            select(Post).where(Post.id == id, Post.deleted_at.is_(None), Post.user_id == user_id)
        )
        post = result.unique().scalar_one_or_none()
        if not post:
            raise RepositoryNotFoundException(f"Not found post with id {id} for the user with id {user_id}")
        post.soft_delete()
        await self.session.commit()
