from typing import List

from models.models import Comment
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class UseCasesComment:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_comment(self, comment: CommentIn) -> Comment:
        return await self.repository.create(comment)

    async def get_comment(self, id: int) -> Comment:
        return await self.repository.get_by_id(id)

    async def get_all_comments(self) -> List[Comment]:
        return await self.repository.get_all()

    async def update_comment(self, id: int, comment: CommentPut) -> Comment:
        return await self.repository.update(id, comment)

    async def delete_comment(self, id: int) -> None:
        await self.repository.delete(id)
