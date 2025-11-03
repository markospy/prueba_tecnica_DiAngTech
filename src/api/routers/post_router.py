from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import get_current_user
from core.database import get_async_session
from repositories.post.repository_post_postgres import RepositoryPostPostgres
from schemas.post import PostIn, PostOut, PostPut
from schemas.security import User
from services.use_cases_post import UseCasesPost

post_router = APIRouter(prefix="/posts", tags=["posts"])


# Dependencia para obtener una instancia de UseCasesPost
async def get_use_cases_post(session: AsyncSession = Depends(get_async_session)) -> UseCasesPost:
    repository = RepositoryPostPostgres(session=session)
    return UseCasesPost(repository=repository)


@post_router.post("/", response_model=PostOut)
async def create_post(
    post: PostIn,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Create a new post
    """
    return await use_cases_post.create_post(post)


@post_router.get("/", response_model=List[PostOut])
async def get_all_posts(
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Get all posts
    """
    return await use_cases_post.get_all_posts()


@post_router.get("/{id}", response_model=PostOut)
async def get_post(
    id: int,
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Get the post by id
    """
    return await use_cases_post.get_post(id)


@post_router.put("/{id}", response_model=PostOut)
async def update_post(
    id: int,
    post: PostPut,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Update the post by id if the user is the owner of the post
    """
    return await use_cases_post.update_post(id, post)


@post_router.delete("/{id}")
async def delete_post(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Delete the post by id if the user is the owner of the post
    """
    await use_cases_post.delete_post(id)
