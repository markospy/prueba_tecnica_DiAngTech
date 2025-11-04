from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.models import Tag
from repositories.exceptions import RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.tags import TagIn, TagPut


class RepositoryTagPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self) -> Optional[List[Tag]]:
        result = await self.session.execute(select(Tag).where(Tag.deleted_at.is_(None)))
        tags = result.unique().scalars().all()
        if not tags:
            raise RepositoryNotFoundException("Not found tags")
        return tags

    async def get_by_id(self, id: int) -> Optional[Tag]:
        result = await self.session.execute(select(Tag).where(Tag.id == id, Tag.deleted_at.is_(None)))
        tag = result.unique().scalar_one_or_none()
        if not tag:
            raise RepositoryNotFoundException(entity_name="Tag", id=id)
        return tag

    async def create(self, schema: TagIn, user_id: int) -> Optional[Tag]:
        tag = Tag(**schema.model_dump(), user_id=user_id)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def update(self, id: int, schema: TagPut, user_id: int) -> Optional[Tag]:
        result = await self.session.execute(
            select(Tag).where(Tag.id == id, Tag.deleted_at.is_(None), Tag.user_id == user_id)
        )
        tag = result.unique().scalar_one_or_none()
        if not tag:
            raise RepositoryNotFoundException(f"Not found tag with id {id} for the user with id {user_id}")
        update_tag_data = schema.model_dump(exclude_unset=True)
        # Actualizar los atributos del tag existente
        for key, value in update_tag_data.items():
            setattr(tag, key, value)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def delete(self, id: int, user_id: int) -> None:
        result = await self.session.execute(
            select(Tag)
            .options(joinedload(Tag.posts))
            .where(Tag.id == id, Tag.deleted_at.is_(None), Tag.user_id == user_id)
        )
        tag = result.unique().scalar_one_or_none()
        if not tag:
            raise RepositoryNotFoundException(f"Not found tag with id {id} for the user with id {user_id}")
        tag.soft_delete()
        tag.posts.clear()
        await self.session.commit()
