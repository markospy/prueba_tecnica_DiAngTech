from typing import List

from models.models import Post
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class UseCasesPost:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_post(self, post: PostIn) -> Post:
        return await self.repository.create(post)

    async def get_post(self, id: int) -> Post:
        return await self.repository.get_by_id(id)

    async def get_all_posts(self) -> List[Post]:
        return await self.repository.get_all()

    async def update_post(self, id: int, post: PostPut) -> Post:
        return await self.repository.update(id, post)

    async def delete_post(self, id: int) -> None:
        await self.repository.delete(id)
