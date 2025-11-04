from typing import List

from src.models.models import Tag
from src.repositories.repository_base import RepositoryBase
from src.schemas.tags import TagIn, TagPut


class UseCasesTag:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_tag(self, tag: TagIn, user_id: int) -> Tag:
        return await self.repository.create(tag, user_id)

    async def get_tag(self, id: int) -> Tag:
        return await self.repository.get_by_id(id)

    async def get_all_tags(self) -> List[Tag]:
        return await self.repository.get_all()

    async def update_tag(self, id: int, tag: TagPut, user_id: int) -> Tag:
        return await self.repository.update(id, tag, user_id)

    async def delete_tag(self, id: int, user_id: int) -> None:
        await self.repository.delete(id, user_id)
