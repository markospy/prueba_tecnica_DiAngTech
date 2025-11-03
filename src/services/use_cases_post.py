from typing import List, Sequence

from models.models import Post
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class UseCasesPost:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_post(self, post: PostIn, user_id: int) -> Post:
        return await self.repository.create(post, user_id)

    async def get_post(self, id: int) -> Post:
        return await self.repository.get_by_id(id)

    async def get_all_posts(self, page: int = 1, size: int = 10) -> tuple[Sequence[Post], int]:
        return await self.repository.get_all(page, size)

    async def update_post(self, id: int, post: PostPut, user_id: int) -> Post:
        return await self.repository.update(id, post, user_id)

    async def delete_post(self, id: int, user_id: int) -> None:
        await self.repository.delete(id, user_id)

    async def get_posts_by_user(self, user_id: int) -> List[Post]:
        return await self.repository.get_by_user_id(user_id)

    async def get_posts_by_tag(self, tag: str) -> List[Post]:
        return await self.repository.get_by_tag(tag)
