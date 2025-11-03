import os
import sys

import pytest  # type: ignore

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.models import Tag
from repositories.exceptions import RepositoryNotFoundException
from repositories.tag.repository_tag_memory import RepositoryTagMemory
from schemas.tags import TagIn, TagPut
from services.use_cases_tag import UseCasesTag


@pytest.fixture
def use_cases_tag():
    return UseCasesTag(RepositoryTagMemory())


@pytest.fixture
def tag():
    return TagIn(name="This is a test tag")


@pytest.fixture
def tag_put():
    return TagPut(name="This is a test tag edited")


@pytest.fixture
def use_cases_tag_with_data():
    memory_db = {1: Tag(id=1, name="This is a test tag")}
    repository = RepositoryTagMemory(memory_db)
    return UseCasesTag(repository)


@pytest.mark.tag
async def test_create_tag(use_cases_tag: UseCasesTag, tag: TagIn):
    tag = await use_cases_tag.create_tag(tag)
    assert tag.name == "This is a test tag"


@pytest.mark.tag
async def test_get_tag(use_cases_tag_with_data: UseCasesTag, tag: TagIn):
    tag_model = await use_cases_tag_with_data.get_tag(1)
    assert tag_model.name == "This is a test tag"


@pytest.mark.tag
async def test_get_all_tags(use_cases_tag_with_data: UseCasesTag, tag: TagIn):
    tags = await use_cases_tag_with_data.get_all_tags()
    assert len(tags) == 1
    assert tags[0].name == "This is a test tag"


@pytest.mark.tag
async def test_update_tag(use_cases_tag_with_data: UseCasesTag, tag_put: TagPut):
    tag_model = await use_cases_tag_with_data.update_tag(1, tag_put)
    assert tag_model.name == "This is a test tag edited"


@pytest.mark.comment
async def test_delete_tag(use_cases_tag_with_data: UseCasesTag, tag: TagIn):
    await use_cases_tag_with_data.delete_tag(1)
    tag_deleted = await use_cases_tag_with_data.get_tag(1)
    assert tag_deleted.deleted_at is not None


@pytest.mark.tag
async def test_not_found_tag(use_cases_tag: UseCasesTag, tag: TagIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_tag.get_tag(2)


@pytest.mark.tag
async def test_not_found_tag_update(use_cases_tag: UseCasesTag, tag: TagPut):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_tag.update_tag(2, tag_put)


@pytest.mark.tag
async def test_not_found_tag_delete(use_cases_tag: UseCasesTag, tag: TagIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_tag.delete_tag(2)
