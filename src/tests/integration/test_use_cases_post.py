import os
import sys

import pytest  # type: ignore

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.models import Post
from repositories.exceptions import RepositoryNotFoundException
from repositories.repository_post_memory import RepositoryPostMemory
from schemas.post import PostIn, PostPut
from services.use_cases_post import UseCasesPost


@pytest.fixture
def use_cases_post():
    return UseCasesPost(RepositoryPostMemory())


@pytest.fixture
def post():
    return PostIn(title="Test Post", content="This is a test post", user_id=1)


@pytest.fixture
def post_put():
    return PostPut(title="Test Post Edited", content="This is a test post edited")


@pytest.fixture
def repository_with_posts():
    memory_db = {1: Post(id=1, title="Test Post", content="This is a test post", user_id=1)}
    return RepositoryPostMemory(memory_db)


@pytest.mark.post
def test_create_post(use_cases_post: UseCasesPost, post: PostIn):
    post = use_cases_post.create_post(post)
    assert post.title == "Test Post"
    assert post.content == "This is a test post"
    assert post.user_id == 1


@pytest.mark.post
def test_get_post(use_cases_post: UseCasesPost, post: PostIn):
    post_model = use_cases_post.get_post(1)
    assert post_model.title == "Test Post"
    assert post_model.content == "This is a test post"
    assert post_model.user_id == 1
    assert post_model.id == 1


@pytest.mark.post
def test_get_all_posts(use_cases_post: UseCasesPost, post: PostIn):
    posts = use_cases_post.get_all_posts()
    assert len(posts) == 1
    assert posts[1].title == "Test Post"
    assert posts[1].content == "This is a test post"
    assert posts[1].user_id == 1
    assert posts[1].id == 1


@pytest.mark.post
def test_update_post(use_cases_post: UseCasesPost, post_put: PostPut):
    post_model = use_cases_post.update_post(1, post_put)
    assert post_model.title == "Test Post Edited"
    assert post_model.content == "This is a test post edited"
    assert post_model.user_id == 1
    assert post_model.id == 1


@pytest.mark.post
def test_delete_post(use_cases_post: UseCasesPost, post: PostIn):
    use_cases_post.delete_post(1)
    post_deleted = use_cases_post.get_post(1)
    assert post_deleted.deleted_at is not None


@pytest.mark.post
def test_not_found_post(use_cases_post: UseCasesPost, post: PostIn):
    with pytest.raises(RepositoryNotFoundException):
        use_cases_post.get_post(2)


@pytest.mark.post
def test_not_found_post_update(use_cases_post: UseCasesPost, post: PostPut):
    with pytest.raises(RepositoryNotFoundException):
        use_cases_post.update_post(2, post_put)


@pytest.mark.post
def test_not_found_post_delete(use_cases_post: UseCasesPost, post: PostIn):
    with pytest.raises(RepositoryNotFoundException):
        use_cases_post.delete_post(2)
