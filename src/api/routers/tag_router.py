from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import get_current_user
from core.database import get_async_session
from repositories.tag.repository_tag_postgres import RepositoryTagPostgres
from schemas.security import User
from schemas.tags import TagIn, TagOut
from services.use_cases_tag import UseCasesTag

tag_router = APIRouter(prefix="/tags", tags=["tags"])


# Dependencia para obtener una instancia de UseCasesComment
async def get_use_cases_tag(session: AsyncSession = Depends(get_async_session)) -> UseCasesTag:
    repository = RepositoryTagPostgres(session=session)
    return UseCasesTag(repository=repository)


@tag_router.post("/", response_model=TagOut)
async def create_tag(
    tag: TagIn,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_tag: UseCasesTag = Depends(get_use_cases_tag),
):
    """
    Create a new tag
    """
    return await use_cases_tag.create_tag(tag)


@tag_router.get("/", response_model=List[TagOut])
async def get_all_tags(
    use_cases_tag: UseCasesTag = Depends(get_use_cases_tag),
):
    """
    Get all tags
    """
    return await use_cases_tag.get_all_tags()


@tag_router.get("/{id}", response_model=TagOut)
async def get_tag(
    id: int,
    use_cases_tag: UseCasesTag = Depends(get_use_cases_tag),
):
    """
    Get the tag by id
    """
    return await use_cases_tag.get_tag(id)


@tag_router.put("/{id}", response_model=TagOut)
async def update_tag(
    id: int,
    tag: TagIn,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_tag: UseCasesTag = Depends(get_use_cases_tag),
):
    """
    Update the tag by id if the user is the owner of the tag
    """
    return await use_cases_tag.update_tag(id, tag)


@tag_router.delete("/{id}")
async def delete_tag(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_tag: UseCasesTag = Depends(get_use_cases_tag),
):
    """
    Delete the tag by id if the user is the owner of the tag
    """
    await use_cases_tag.delete_tag(id)
