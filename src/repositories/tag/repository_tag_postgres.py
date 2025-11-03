from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Tag
from repositories.exceptions import RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.tags import TagIn, TagPut


class RepositoryTagPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self) -> Optional[List[Tag]]:
        result = await Tag.all_active(self.session)
        if not result:
            raise RepositoryNotFoundException("Tag", "all")
        return result

    async def get_by_id(self, id: int) -> Optional[Tag]:
        tag = await Tag.get_by_id(self.session, id)
        if not tag:
            raise RepositoryNotFoundException("Tag", id)
        return tag

    async def create(self, schema: TagIn) -> Optional[Tag]:
        tag = Tag(**schema.model_dump())
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def update(self, id: int, schema: TagPut) -> Optional[Tag]:
        tag: Tag | None = await Tag.get_by_id(self.session, id)
        if not tag:
            raise RepositoryNotFoundException("Tag", id)
        update_tag_data = schema.model_dump(exclude_unset=True)
        update_tag = tag.model_copy(update=update_tag_data)
        self.session.add(update_tag)
        await self.session.commit()
        await self.session.refresh(update_tag)
        return update_tag

    async def delete(self, id: int) -> None:
        tag: Tag | None = await Tag.get_by_id(self.session, id)
        if not tag:
            raise RepositoryNotFoundException("Tag", id)
        tag.soft_delete()
        await self.session.commit()
