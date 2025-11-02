from typing import List

from models.models import Post
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class UseCasesPost:
    def __init__(self, repository: RepositoryBase):
        self.repository = repository

    def create_post(self, post: PostIn) -> Post:
        return self.repository.create(post)

    def get_post(self, id: int) -> Post:
        return self.repository.get_by_id(id)

    def get_all_posts(self) -> List[Post]:
        return self.repository.get_all()

    def update_post(self, id: int, post: PostPut) -> Post:
        return self.repository.update(id, post)

    def delete_post(self, id: int) -> None:
        self.repository.delete(id)
