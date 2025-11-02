from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.models import User
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.user import UserIn, UserPut


class RepositoryUserPostgres(RepositoryBase):

    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self) -> Optional[List[User]]:
        return User.all_active(self.session).all()

    def get_by_id(self, id: int) -> Optional[User]:
        return User.get_by_id(self.session, id)

    def create(self, schema: UserIn) -> Optional[User]:
        user = User(**schema.model_dump())
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError:
            self.session.rollback()
            raise RepositoryAlreadyExistsException("User", user.username)

    def update(self, id: int, schema: UserPut) -> Optional[User]:
        user: User | None = User.get_by_id(self.session, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        update_user_data = schema.model_dump(exclude_unset=True)
        update_user = user.model_copy(update=update_user_data)
        self.session.add(update_user)
        self.session.commit()
        self.session.refresh(update_user)
        return update_user

    def delete(self, id: int) -> None:
        user = User.get_by_id(self.session, id)
        if not user:
            raise RepositoryNotFoundException("User", id)
        user.soft_delete()
        self.session.commit()
