from typing import Optional

from models.models import Comment
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class RepositoryCommentMemory(RepositoryBase):
    def __init__(self, comments: dict[int, Comment] = {}):
        self.comments: dict[int, Comment] = comments
        self.id_counter = 0

    def get_all(self) -> dict[int, Comment]:
        return self.comments

    def get_by_id(self, id: int) -> Optional[Comment]:
        comment = self.comments.get(id)
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        return comment

    def create(self, comment: CommentIn) -> Optional[Comment]:
        if self.get_by_content(comment.content):
            raise RepositoryAlreadyExistsException("Comment", comment.content)
        comment_in_dict = comment.model_dump()
        comment_in_dict["id"] = self.increment_id_counter()
        comment_model = Comment(**comment_in_dict)
        self.comments[comment_model.id] = comment_model
        return comment_model

    def update(self, id: int, comment: CommentPut) -> Optional[Comment]:
        stored_comment = self.comments.get(id)
        if not stored_comment:
            raise RepositoryNotFoundException("Comment", id)

        # Actualizar los atributos del comment existente
        update_data = comment.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_comment, key, value)

        return stored_comment

    def delete(self, id: int) -> None:
        if not self.comments.get(id):
            raise RepositoryNotFoundException("Comment", id)
        self.comments[id].soft_delete()

    def increment_id_counter(self) -> int:
        self.id_counter += 1
        return self.id_counter

    def get_by_content(self, content: str) -> Optional[Comment]:
        return next((comment for comment in self.comments.values() if comment.content == content), None)
