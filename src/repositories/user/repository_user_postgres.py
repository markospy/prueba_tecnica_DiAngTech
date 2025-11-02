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
        with self.session as session:
            return User.all_active(session).all()

    def get_by_id(self, id: int) -> Optional[User]:
        with self.session as session:
            return User.get_by_id(session, id)

    def create(self, schema: UserIn) -> Optional[User]:
        user = User(**schema.model_dump())
        with self.session as session:
            try:
                session.add(user)
                session.commit()
                return user
            except IntegrityError:
                session.rollback()
                raise RepositoryAlreadyExistsException("User", user.username)

    def update(self, id: int, schema: UserPut) -> Optional[User]:
        with self.session as session:
            user: User | None = User.get_by_id(session, id)
            if not user:
                raise RepositoryNotFoundException("User", id)
            update_user_data = schema.model_dump(exclude_unset=True)
            update_user = user.model_copy(update=update_user_data)
            session.add(update_user)
            session.commit()
            return user

    def delete(self, id: int) -> None:
        with self.session as session:
            user = User.get_by_id(session, id)
            if not user:
                raise RepositoryNotFoundException("User", id)
            user.soft_delete()
            session.commit()
