from typing import List

from models.models import User
from repositories.repository_base import RepositoryBase
from schemas.user import UserIn, UserPut


class UseCasesUser:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_user(self, user: UserIn) -> User:
        return await self.repository.create(user)

    async def get_user(self, id: int) -> User:
        return await self.repository.get_by_id(id)

    async def get_all_users(self) -> List[User]:
        return await self.repository.get_all()

    async def update_user(self, id: int, user: UserPut) -> User:
        return await self.repository.update(id, user)

    async def delete_user(self, id: int) -> None:
        await self.repository.delete(id)

    async def authenticate_user(self, username: str, password: str) -> str:
        return await self.repository.authenticate_user(username, password)
