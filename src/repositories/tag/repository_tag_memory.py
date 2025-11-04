from typing import List, Optional

from src.models.models import Tag
from src.repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from src.repositories.repository_base import RepositoryBase
from src.schemas.tags import TagIn, TagPut


class RepositoryTagMemory(RepositoryBase):
    def __init__(self, tags: dict[int, Tag] = {}, session=None):
        super().__init__(session=session)
        self.tags: dict[int, Tag] = tags
        self.id_counter = 0

    async def get_all(self) -> Optional[List[Tag]]:
        return list(self.tags.values())

    async def get_by_id(self, id: int) -> Optional[Tag]:
        tag = self.tags.get(id)
        if not tag:
            raise RepositoryNotFoundException(entity_name="Tag", id=id)
        return tag

    async def create(self, tag: TagIn) -> Optional[Tag]:
        if self.get_by_name(tag.name):
            raise RepositoryAlreadyExistsException(entity_name="Tag", name=tag.name)
        tag_in_dict = tag.model_dump()
        tag_in_dict["id"] = self.increment_id_counter()
        tag_model = Tag(**tag_in_dict)
        self.tags[tag_model.id] = tag_model
        return tag_model

    async def update(self, id: int, tag: TagPut) -> Optional[Tag]:
        stored_tag = self.tags.get(id)
        if not stored_tag:
            raise RepositoryNotFoundException(entity_name="Tag", id=id)

        # Actualizar los atributos del tag existente
        update_data = tag.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_tag, key, value)

        return stored_tag

    async def delete(self, id: int) -> None:
        if not self.tags.get(id):
            raise RepositoryNotFoundException(entity_name="Tag", id=id)
        self.tags[id].soft_delete()

    def increment_id_counter(self) -> int:
        self.id_counter += 1
        return self.id_counter

    def get_by_name(self, name: str) -> Optional[Tag]:
        return next((tag for tag in self.tags.values() if tag.name == name), None)
