from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import get_by_username, get_password_hash, verify_password
from models.models import User
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.security import UserInDB
from schemas.user import UserIn, UserPut


class RepositoryUserPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self) -> Optional[List[User]]:
        result = await User.all_active(self.session)
        if not result:
            raise RepositoryNotFoundException("User", "all")
        return result

    async def get_by_id(self, id: int) -> Optional[User]:
        user = await self.session.get(User, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        return user

    async def create(self, schema: UserIn) -> Optional[User]:
        user_dict = schema.model_dump()
        user_dict["password"] = get_password_hash(schema.password)
        user = User(**user_dict)
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise RepositoryAlreadyExistsException("User", user.username)

    async def update(self, id: int, schema: UserPut) -> Optional[User]:
        user: User | None = await self.session.get(User, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        update_user_data = schema.model_dump(exclude_unset=True)
        # Actualizar los atributos del usuario existente
        for key, value in update_user_data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, id: int) -> None:
        user: User | None = await self.session.get(User, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        user.soft_delete()
        await self.session.commit()

    async def authenticate_user(self, username: str, password: str) -> UserInDB:
        user: UserInDB | None = await get_by_username(self.session, username)
        if not user:
            return None
        if verify_password(password, user.hashed_password):
            return user
        return None
