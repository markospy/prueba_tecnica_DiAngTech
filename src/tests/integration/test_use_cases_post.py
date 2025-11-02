import os
import sys

import pytest  # type: ignore

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from models.models import Post
from repositories.repository_post_memory import RepositoryPostMemory
from schemas.post import PostIn, PostPut
from services.use_cases_post import create_post, delete_post, get_all_posts, get_post, update_post


@pytest.fixture
def repository():
    return RepositoryPostMemory()


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
def test_create_post(repository: RepositoryPostMemory, post: PostIn):
    post = create_post(post, repository)
    assert post.title == "Test Post"
    assert post.content == "This is a test post"
    assert post.user_id == 1


@pytest.mark.post
def test_get_post(repository_with_posts: RepositoryPostMemory, post: PostIn):
    post_model = get_post(1, repository_with_posts)
    assert post_model.title == "Test Post"
    assert post_model.content == "This is a test post"
    assert post_model.user_id == 1
    assert post_model.id == 1


@pytest.mark.post
def test_get_all_posts(repository_with_posts: RepositoryPostMemory, post: PostIn):
    posts = get_all_posts(repository_with_posts)
    assert len(posts) == 1
    assert posts[1].title == "Test Post"
    assert posts[1].content == "This is a test post"
    assert posts[1].user_id == 1
    assert posts[1].id == 1


@pytest.mark.post
def test_update_post(repository_with_posts: RepositoryPostMemory, post_put: PostPut):
    post_model = update_post(1, post_put, repository_with_posts)
    assert post_model.title == "Test Post Edited"
    assert post_model.content == "This is a test post edited"
    assert post_model.user_id == 1
    assert post_model.id == 1


@pytest.mark.post
def test_delete_post(repository_with_posts: RepositoryPostMemory, post: PostIn):
    delete_post(1, repository_with_posts)
    post_deleted = repository_with_posts.get_by_id(1)
    assert post_deleted.deleted_at is not None
