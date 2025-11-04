from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Comment
from repositories.exceptions import RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.comment import CommentIn, CommentPut


class RepositoryCommentPostgres(RepositoryBase):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all(self, post_id: int, page: int, size: int) -> tuple[List[Comment], int]:
        skip = (page - 1) * size
        base_query = select(Comment).where(Comment.deleted_at.is_(None), Comment.post_id == post_id)

        # Count
        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self.session.scalar(count_query)

        # Comments
        query = base_query.offset(skip).limit(size).order_by(Comment.created_at.desc())
        result = await self.session.execute(query)
        posts = result.unique().scalars().all()

        return posts, total

    async def get_by_id(self, id: int) -> Optional[Comment]:
        result = await self.session.execute(select(Comment).where(Comment.id == id, Comment.deleted_at.is_(None)))
        comment = result.unique().scalar_one_or_none()
        if not comment:
            raise RepositoryNotFoundException("Comment", id)
        return comment

    async def create(self, schema: CommentIn, user_id: int, post_id: int) -> Optional[Comment]:
        comment = Comment(**schema.model_dump(), user_id=user_id, post_id=post_id)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def update(self, id: int, schema: CommentPut, user_id: int) -> Optional[Comment]:
        result = await self.session.execute(
            select(Comment).where(Comment.id == id, Comment.deleted_at.is_(None), Comment.user_id == user_id)
        )
        comment = result.unique().scalar_one_or_none()
        if not comment:
            raise RepositoryNotFoundException(f"Not found comment with id {id} for the user with id {user_id}")
        update_comment_data = schema.model_dump(exclude_unset=True)
        # Actualizar los atributos del comentario existente
        for key, value in update_comment_data.items():
            setattr(comment, key, value)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def delete(self, id: int, user_id: int) -> None:
        result = await self.session.execute(
            select(Comment).where(Comment.id == id, Comment.deleted_at.is_(None), Comment.user_id == user_id)
        )
        comment = result.unique().scalar_one_or_none()
        if not comment:
            raise RepositoryNotFoundException(f"Not found comment with id {id} for the user with id {user_id}")
        comment.soft_delete()
        await self.session.commit()
