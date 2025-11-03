from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.security import get_current_user
from core.database import get_async_session
from repositories.user.repository_user_postgres import RepositoryUserPostgres
from schemas.security import User
from schemas.user import UserOut, UserPut
from services.use_cases_user import UseCasesUser

user_router = APIRouter(prefix="/users", tags=["users"])


# Dependencia para obtener una instancia de UseCasesUser
async def get_use_cases_user(session: AsyncSession = Depends(get_async_session)) -> UseCasesUser:
    repository = RepositoryUserPostgres(session=session)
    return UseCasesUser(repository=repository)


@user_router.get("/{id}", response_model=UserOut)
async def get_user(
    id: int,
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    """
    Get the user by id
    """
    return await use_cases_user.get_user(id)


@user_router.put("/", response_model=UserOut)
async def update_user(
    user: UserPut,
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    """
    Update the current user
    """
    return await use_cases_user.update_user(current_user.id, user)


@user_router.delete("/")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_user)],
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    """
    Delete the current user
    """
    await use_cases_user.delete_user(current_user.id)
