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
        return Comment.all_active(self.session).all()

    def get_by_id(self, id: int) -> Optional[Comment]:
        return Comment.get_by_id(self.session, id)

    def create(self, schema: CommentIn) -> Optional[Comment]:
        comment = Comment(**schema.model_dump())
        try:
            self.session.add(comment)
            self.session.commit()
            self.session.refresh(comment)
            return comment
        except IntegrityError:
            self.session.rollback()
            raise RepositoryAlreadyExistsException("Comment", comment.content)

    def update(self, id: int, schema: CommentPut) -> Optional[Comment]:
        comment: Comment | None = Comment.get_by_id(self.session, id)
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        update_comment_data = schema.model_dump(exclude_unset=True)
        update_comment = comment.model_copy(update=update_comment_data)
        self.session.add(update_comment)
        self.session.commit()
        self.session.refresh(update_comment)
        return update_comment

    def delete(self, id: int) -> None:
        comment = Comment.get_by_id(self.session, id)
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        comment.soft_delete()
        self.session.commit()
