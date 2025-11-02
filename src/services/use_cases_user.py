from typing import List

from models.models import User
from repositories.repository_base import RepositoryBase
from schemas.user import UserIn, UserPut


class UseCasesUser:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    def create_user(self, user: UserIn) -> User:
        return self.repository.create(user)

    def get_user(self, id: int) -> User:
        return self.repository.get_by_id(id)

    def get_all_users(self) -> List[User]:
        return self.repository.get_all()

    def update_user(self, id: int, user: UserPut) -> User:
        return self.repository.update(id, user)

    def delete_user(self, id: int) -> None:
        self.repository.delete(id)
