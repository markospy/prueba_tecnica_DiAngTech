from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import get_current_user
from core.database import get_async_session
from repositories.comment.repository_comment_postgres import RepositoryCommentPostgres
from schemas.comment import CommentIn, CommentOut, CommentPut
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
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Create a new comment
    """
    return await use_cases_comment.create_comment(comment)


@comment_router.get("/", response_model=List[CommentOut])
async def get_all_comments(
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Get all comments
    """
    return await use_cases_comment.get_all_comments()


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
    return await use_cases_comment.update_comment(id, comment)


@comment_router.delete("/{id}")
async def delete_comment(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    """
    Delete the comment by id if the user is the owner of the comment
    """
    await use_cases_comment.delete_comment(id)
