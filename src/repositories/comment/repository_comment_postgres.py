from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Comment
from repositories.exceptions import RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class RepositoryCommentPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self) -> Optional[List[Comment]]:
        result = await Comment.all_active(self.session)
        if not result:
            raise RepositoryNotFoundException("Comment", "all")
        return result

    async def get_by_id(self, id: int) -> Optional[Comment]:
        comment = await Comment.get_by_id(self.session, id)
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        return comment

    async def create(self, schema: CommentIn) -> Optional[Comment]:
        comment = Comment(**schema.model_dump())
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def update(self, id: int, schema: CommentPut) -> Optional[Comment]:
        comment: Comment | None = await Comment.get_by_id(self.session, id)
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        update_comment_data = schema.model_dump(exclude_unset=True)
        update_comment = comment.model_copy(update=update_comment_data)
        self.session.add(update_comment)
        await self.session.commit()
        await self.session.refresh(update_comment)
        return update_comment

    async def delete(self, id: int) -> None:
        comment: Comment | None = await Comment.get_by_id(self.session, id)
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        comment.soft_delete()
        await self.session.commit()
