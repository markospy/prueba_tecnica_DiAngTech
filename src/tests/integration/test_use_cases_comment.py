import os
import sys

import pytest  # type: ignore

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.models import Comment
from repositories.comment.repository_comment_memory import RepositoryCommentMemory
from repositories.exceptions import RepositoryNotFoundException
from schemas.comment import CommentIn, CommentPut
from services.use_cases_comment import UseCasesComment


@pytest.fixture
def use_cases_comment():
    return UseCasesComment(RepositoryCommentMemory())


@pytest.fixture
def comment():
    return CommentIn(content="This is a test comment", user_id=1, post_id=1)


@pytest.fixture
def comment_put():
    return CommentPut(content="This is a test comment edited")


@pytest.fixture
def use_cases_comment_with_data():
    memory_db = {1: Comment(id=1, content="This is a test comment", user_id=1, post_id=1)}
    repository = RepositoryCommentMemory(memory_db)
    return UseCasesComment(repository)


@pytest.mark.comment
async def test_create_comment(use_cases_comment: UseCasesComment, comment: CommentIn):
    comment = await use_cases_comment.create_comment(comment)
    assert comment.content == "This is a test comment"
    assert comment.user_id == 1
    assert comment.post_id == 1


@pytest.mark.comment
async def test_get_comment(use_cases_comment_with_data: UseCasesComment, comment: CommentIn):
    comment_model = await use_cases_comment_with_data.get_comment(1)
    assert comment_model.content == "This is a test comment"
    assert comment_model.user_id == 1
    assert comment_model.post_id == 1


@pytest.mark.comment
async def test_get_all_comments(use_cases_comment_with_data: UseCasesComment, comment: CommentIn):
    comments = await use_cases_comment_with_data.get_all_comments()
    assert len(comments) == 1
    assert comments[0].content == "This is a test comment"
    assert comments[0].user_id == 1
    assert comments[0].post_id == 1


@pytest.mark.comment
async def test_update_comment(use_cases_comment_with_data: UseCasesComment, comment_put: CommentPut):
    comment_model = await use_cases_comment_with_data.update_comment(1, comment_put)
    assert comment_model.content == "This is a test comment edited"
    assert comment_model.user_id == 1
    assert comment_model.post_id == 1


@pytest.mark.comment
async def test_delete_comment(use_cases_comment_with_data: UseCasesComment, comment: CommentIn):
    await use_cases_comment_with_data.delete_comment(1)
    comment_deleted = await use_cases_comment_with_data.get_comment(1)
    assert comment_deleted.deleted_at is not None


@pytest.mark.comment
async def test_not_found_comment(use_cases_comment: UseCasesComment, comment: CommentIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_comment.get_comment(2)


@pytest.mark.comment
async def test_not_found_comment_update(use_cases_comment: UseCasesComment, comment: CommentPut):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_comment.update_comment(2, comment_put)


@pytest.mark.comment
async def test_not_found_comment_delete(use_cases_comment: UseCasesComment, comment: CommentIn):
    with pytest.raises(RepositoryNotFoundException):
        await use_cases_comment.delete_comment(2)
