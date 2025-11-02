from typing import List

from models.models import Post
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn


def create_post(post: PostIn, repository: RepositoryBase) -> Post:
    return repository.create(post)


def get_post(id: int, repository: RepositoryBase) -> Post:
    return repository.get_by_id(id)


def get_all_posts(repository: RepositoryBase) -> List[Post]:
    return repository.get_all()


def update_post(id: int, post: PostIn, repository: RepositoryBase) -> Post:
    return repository.update(id, post)


def delete_post(id: int, repository: RepositoryBase) -> None:
    return repository.delete(id)
