from typing import List

from models.models import Comment
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class UseCasesComment:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    def create_comment(self, comment: CommentIn) -> Comment:
        return self.repository.create(comment)

    def get_comment(self, id: int) -> Comment:
        return self.repository.get_by_id(id)

    def get_all_comments(self) -> List[Comment]:
        return self.repository.get_all()

    def update_comment(self, id: int, comment: CommentPut) -> Comment:
        return self.repository.update(id, comment)

    def delete_comment(self, id: int) -> None:
        self.repository.delete(id)
