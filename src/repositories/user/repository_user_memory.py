from typing import List, Optional

from models.models import User
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.user import UserIn, UserPut


class RepositoryUserMemory(RepositoryBase):
    def __init__(self, users: dict[int, User] = {}, session=None):
        super().__init__(session=session)
        self.users: dict[int, User] = users
        self.id_counter = 0

    async def get_all(self) -> Optional[List[User]]:
        return list(self.users.values())

    async def get_by_id(self, id: int) -> Optional[User]:
        user = self.users.get(id)
        if not user:
            raise RepositoryNotFoundException(entity_name="User", id=id)
        return user

    async def create(self, user: UserIn) -> Optional[User]:
        existing_user = await self.get_by_username(user.username)
        if existing_user:
            raise RepositoryAlreadyExistsException(entity_name="User", name=user.username)
        user_in_dict = user.model_dump()
        user_in_dict["id"] = self.increment_id_counter()
        user_model = User(**user_in_dict)
        self.users[user_model.id] = user_model
        return user_model

    async def update(self, id: int, user: UserPut) -> Optional[User]:
        stored_user = self.users.get(id)
        if not stored_user:
            raise RepositoryNotFoundException(entity_name="User", id=id)

        # Actualizar los atributos del user existente
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_user, key, value)

        return stored_user

    async def delete(self, id: int) -> None:
        if not self.users.get(id):
            raise RepositoryNotFoundException(entity_name="User", id=id)
        self.users[id].soft_delete()

    def increment_id_counter(self) -> int:
        self.id_counter += 1
        return self.id_counter

    async def get_by_username(self, username: str) -> Optional[User]:
        return next((user for user in self.users.values() if user.username == username), None)
