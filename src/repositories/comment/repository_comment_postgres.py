from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.models import Comment
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class RepositoryCommentPostgres(RepositoryBase):

    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self) -> Optional[List[Comment]]:
        with self.session as session:
            return Comment.all_active(session).all()

    def get_by_id(self, id: int) -> Optional[Comment]:
        with self.session as session:
            return Comment.get_by_id(session, id)

    def create(self, schema: CommentIn) -> Optional[Comment]:
        comment = Comment(**schema.model_dump())
        with self.session as session:
            try:
                session.add(comment)
                session.commit()
                return comment
            except IntegrityError:
                session.rollback()
                raise RepositoryAlreadyExistsException("Comment", comment.content)

    def update(self, id: int, schema: CommentPut) -> Optional[Comment]:
        with self.session as session:
            comment: Comment | None = Comment.get_by_id(session, id)
            if not comment:
                raise RepositoryNotFoundException("Comment", id)
            update_comment_data = schema.model_dump(exclude_unset=True)
            update_comment = comment.model_copy(update=update_comment_data)
            session.add(update_comment)
            session.commit()
            return comment

    def delete(self, id: int) -> None:
        with self.session as session:
            comment = Comment.get_by_id(session, id)
            if not comment:
                raise RepositoryNotFoundException("Comment", id)
            comment.soft_delete()
            session.commit()
