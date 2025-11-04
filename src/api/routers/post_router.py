import math
from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.security import get_current_user
from src.core.database import get_async_session
from src.repositories.post.repository_post_postgres import RepositoryPostPostgres
from src.schemas.pagination import PaginatedResponse
from src.schemas.post import PostIn, PostOut, PostPut
from src.schemas.security import User
from src.services.use_cases_post import UseCasesPost

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
    return await use_cases_post.create_post(post, current_user.id)


@post_router.get("/", response_model=PaginatedResponse[PostOut])
async def get_all_posts(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Get all posts

    - **page**: Number of page (starts at 1)
    - **size**: Number of items per page (maximum 100)
    """
    posts, total = await use_cases_post.get_all_posts(page=page, size=size)

    return PaginatedResponse(
        items=posts,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 0,
    )


@post_router.get("/{id}", response_model=PostOut)
async def get_post(
    id: int,
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Get the post by id
    """
    return await use_cases_post.get_post(id)


@post_router.get("/user/{user_id}", response_model=List[PostOut])
async def get_posts_by_user(
    user_id: int,
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Get the posts by user id
    """
    return await use_cases_post.get_posts_by_user(user_id)


@post_router.get("/tag/{tag}", response_model=List[PostOut])
async def get_posts_by_tag(
    tag: str,
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Get the posts by tag
    """
    return await use_cases_post.get_posts_by_tag(tag)


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
    return await use_cases_post.update_post(id, post, current_user.id)


@post_router.delete("/{id}")
async def delete_post(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_post: UseCasesPost = Depends(get_use_cases_post),
):
    """
    Delete the post by id if the user is the owner of the post
    """
    await use_cases_post.delete_post(id, current_user.id)
