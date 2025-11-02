from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
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
        user = await User.get_by_id(self.session, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        return user

    async def create(self, schema: UserIn) -> Optional[User]:
        user = User(**schema.model_dump())
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise RepositoryAlreadyExistsException("User", user.username)

    async def update(self, id: int, schema: UserPut) -> Optional[User]:
        user: User | None = await User.get_by_id(self.session, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        update_user_data = schema.model_dump(exclude_unset=True)
        update_user = user.model_copy(update=update_user_data)
        self.session.add(update_user)
        await self.session.commit()
        await self.session.refresh(update_user)
        return update_user

    async def delete(self, id: int) -> None:
        user: User | None = await User.get_by_id(self.session, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        user.soft_delete()
        await self.session.commit()
