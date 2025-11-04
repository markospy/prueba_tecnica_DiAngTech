from typing import Sequence

from models.models import Comment
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class UseCasesComment:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    async def create_comment(self, comment: CommentIn, user_id: int, post_id: int) -> Comment:
        return await self.repository.create(comment, user_id, post_id)

    async def get_comment(self, id: int) -> Comment:
        return await self.repository.get_by_id(id)

    async def get_all_comments(self, post_id: int, page: int = 1, size: int = 10) -> tuple[Sequence[Comment], int]:
        return await self.repository.get_all(post_id, page, size)

    async def update_comment(self, id: int, comment: CommentPut, user_id: int) -> Comment:
        return await self.repository.update(id, comment, user_id)

    async def delete_comment(self, id: int, user_id: int) -> None:
        await self.repository.delete(id, user_id)
