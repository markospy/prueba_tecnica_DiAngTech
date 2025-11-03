import os
import sys

import pytest  # type: ignore

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.models import User
from repositories.exceptions import RepositoryNotFoundException
from repositories.user.repository_user_memory import RepositoryUserMemory
from schemas.user import UserIn, UserPut
from services.use_cases_user import UseCasesUser


@pytest.fixture
def use_cases_user():
    return UseCasesUser(RepositoryUserMemory())


@pytest.fixture
def user():
    return UserIn(username="Test User", fullname="Test User", email="test@test.com", password="password")


@pytest.fixture
def user_put():
    return UserPut(
        username="Test User Edited", fullname="Test User Edited", email="test@test.com", password="password"
    )


@pytest.fixture
def use_cases_user_with_data():
    memory_db = {1: User(id=1, username="Test User", fullname="Test User", email="test@test.com", password="password")}
    repository = RepositoryUserMemory(memory_db)
    return UseCasesUser(repository)


@pytest.mark.user
async def test_create_user(use_cases_user: UseCasesUser, user: UserIn):
    user_model = await use_cases_user.create_user(user)
    assert user_model.username == "Test User"
    assert user_model.fullname == "Test User"
    assert user_model.id == 2


@pytest.mark.user
async def test_get_user(use_cases_user_with_data: UseCasesUser, user: UserIn):
    user_model = await use_cases_user_with_data.get_user(1)
    assert user_model.username == "Test User"
    assert user_model.fullname == "Test User"
    assert user_model.email == "test@test.com"
    assert user_model.id == 1


@pytest.mark.user
async def test_get_all_users(use_cases_user_with_data: UseCasesUser, user: UserIn):
    users = await use_cases_user_with_data.get_all_users()
    assert len(users) == 1
    assert users[0].username == "Test User"
    assert users[0].fullname == "Test User"
    assert users[0].email == "test@test.com"
    assert users[0].id == 1


@pytest.mark.user
async def test_update_user(use_cases_user_with_data: UseCasesUser, user_put: UserPut):
    user_model = await use_cases_user_with_data.update_user(1, user_put)
    assert user_model.username == "Test User Edited"
    assert user_model.fullname == "Test User Edited"
    assert user_model.email == "test@test.com"
    assert user_model.id == 1


@pytest.mark.user
async def test_delete_user(use_cases_user_with_data: UseCasesUser, user: UserIn):
    await use_cases_user_with_data.delete_user(1)
    user_deleted = await use_cases_user_with_data.get_user(1)
    assert user_deleted.deleted_at is not None


@pytest.mark.user
async def test_not_found_user(use_cases_user_with_data: UseCasesUser, user: UserIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_user_with_data.get_user(2)


@pytest.mark.user
async def test_not_found_user_update(use_cases_user_with_data: UseCasesUser, user: UserIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_user_with_data.update_user(2, user_put)


@pytest.mark.user
async def test_not_found_user_delete(use_cases_user: UseCasesUser, user: UserIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_user.delete_user(2)
