from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Post
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class RepositoryPostPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self) -> Optional[List[Post]]:
        result = await Post.all_active(self.session)
        if not result:
            raise RepositoryNotFoundException("Post", "all")
        return result

    async def get_by_id(self, id: int) -> Optional[Post]:
        post = await Post.get_by_id(self.session, id)
        if not post:
            raise RepositoryNotFoundException("Post", id)
        return post

    async def create(self, schema: PostIn) -> Optional[Post]:
        post = Post(**schema.model_dump())
        try:
            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post)
            return post
        except IntegrityError:
            await self.session.rollback()
            raise RepositoryAlreadyExistsException("Post", post.title)

    async def update(self, id: int, schema: PostPut) -> Optional[Post]:
        post: Post | None = await Post.get_by_id(self.session, id)
        if not post:
            raise RepositoryNotFoundException("Post", id)
        update_post_data = schema.model_dump(exclude_unset=True)
        update_post = post.model_copy(update=update_post_data)
        self.session.add(update_post)
        try:
            await self.session.commit()
            await self.session.refresh(update_post)
            return update_post
        except IntegrityError:
            await self.session.rollback()
            raise RepositoryAlreadyExistsException("Post", update_post.title)

    async def delete(self, id: int) -> None:
        post: Post | None = await Post.get_by_id(self.session, id)
        if not post:
            raise RepositoryNotFoundException("Post", id)
        post.soft_delete()
        await self.session.commit()
