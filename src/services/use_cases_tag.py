from typing import List

from models.models import Tag
from repositories.repository_base import RepositoryBase
from schemas.tags import TagIn, TagPut


class UseCasesTag:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_tag(self, tag: TagIn) -> Tag:
        return await self.repository.create(tag)

    async def get_tag(self, id: int) -> Tag:
        return await self.repository.get_by_id(id)

    async def get_all_tags(self) -> List[Tag]:
        return await self.repository.get_all()

    async def update_tag(self, id: int, tag: TagPut) -> Tag:
        return await self.repository.update(id, tag)

    async def delete_tag(self, id: int) -> None:
        await self.repository.delete(id)
