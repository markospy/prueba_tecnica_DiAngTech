from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_session
from repositories.comment.repository_comment_postgres import RepositoryCommentPostgres
from schemas.comment import CommentIn, CommentOut, CommentPut
from services.use_cases_comment import UseCasesComment

comment_router = APIRouter(prefix="/comments", tags=["comments"])


# Dependencia para obtener una instancia de UseCasesComment
def get_use_cases_comment(session: Session = Depends(get_session)) -> UseCasesComment:
    repository = RepositoryCommentPostgres(session=session)
    return UseCasesComment(repository=repository)


@comment_router.post("/", response_model=CommentOut)
def create_comment(
    comment: CommentIn,
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    return use_cases_comment.create_comment(comment)


@comment_router.get("/", response_model=List[CommentOut])
def get_all_comments(
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    return use_cases_comment.get_all_comments()


@comment_router.get("/{id}", response_model=CommentOut)
def get_comment(
    id: int,
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    return use_cases_comment.get_comment(id)


@comment_router.put("/{id}", response_model=CommentOut)
def update_comment(
    id: int,
    comment: CommentPut,
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    return use_cases_comment.update_comment(id, comment)


@comment_router.delete("/{id}")
def delete_comment(
    id: int,
    use_cases_comment: UseCasesComment = Depends(get_use_cases_comment),
):
    use_cases_comment.delete_comment(id)
