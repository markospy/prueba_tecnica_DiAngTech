import math
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import get_current_user
from core.database import get_async_session
from repositories.comment.repository_comment_postgres import RepositoryCommentPostgres
from schemas.comment import CommentIn, CommentOut, CommentPut
from schemas.pagination import PaginatedResponse
from schemas.security import User
from services.use_cases_comment import UseCasesComment

comment_router = APIRouter(prefix="/comments", tags=["comments"])


# Dependencia para obtener una instancia de UseCasesComment
async def get_use_cases_comment(session: AsyncSession = Depends(get_async_session)) -> UseCasesComment:
    repository = RepositoryCommentPostgres(session=session)
    return UseCasesComment(repository=repository)


@comment_router.post("/", response_model=CommentOut)
async def create_comment(
    comment: CommentIn,
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: int,
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Create a new comment
    """
    return await use_cases_comment.create_comment(comment, current_user.id, post_id)


@comment_router.get("/", response_model=PaginatedResponse[CommentOut])
async def get_all_comments(
    post_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Get all comments of one post

    - **page**: Number of page (starts at 1)
    - **size**: Number of items per page (maximum 100)
    """
    comments, total = await use_cases_comment.get_all_comments(post_id)
    return PaginatedResponse(
        items=comments,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 0,
    )


@comment_router.get("/{id}", response_model=CommentOut)
async def get_comment(
    id: int,
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Get the comment by id
    """
    return await use_cases_comment.get_comment(id)


@comment_router.put("/{id}", response_model=CommentOut)
async def update_comment(
    id: int,
    comment: CommentPut,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Update the comment by id if the user is the owner of the comment
    """
    return await use_cases_comment.update_comment(id, comment, current_user.id)


@comment_router.delete("/{id}")
async def delete_comment(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Delete the comment by id if the user is the owner of the comment
    """
    await use_cases_comment.delete_comment(id, current_user.id)
