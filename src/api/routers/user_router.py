from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from repositories.user.repository_user_postgres import RepositoryUserPostgres
from schemas.user import UserIn, UserOut, UserPut
from services.use_cases_user import UseCasesUser

user_router = APIRouter(prefix="/users", tags=["users"])


# Dependencia para obtener una instancia de UseCasesUser
async def get_use_cases_user(session: AsyncSession = Depends(get_async_session)) -> UseCasesUser:
    repository = RepositoryUserPostgres(session=session)
    return UseCasesUser(repository=repository)


@user_router.post("/", response_model=UserOut)
async def create_user(
    user: UserIn,
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    return await use_cases_user.create_user(user)


@user_router.get("/{id}", response_model=UserOut)
async def get_user(
    id: int,
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    return await use_cases_user.get_user(id)


@user_router.put("/{id}", response_model=UserOut)
async def update_user(
    id: int,
    user: UserPut,
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    return await use_cases_user.update_user(id, user)


@user_router.delete("/{id}")
async def delete_user(
    id: int,
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    await use_cases_user.delete_user(id)
