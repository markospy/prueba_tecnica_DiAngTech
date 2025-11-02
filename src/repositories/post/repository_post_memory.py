from typing import Optional

from models.models import Post
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class RepositoryPostMemory(RepositoryBase):
    def __init__(self, posts: dict[int, Post] = {}):
        self.posts: dict[int, Post] = posts
        self.id_counter = 0

    def get_all(self) -> dict[int, Post]:
        return self.posts

    def get_by_id(self, id: int) -> Optional[Post]:
        post = self.posts.get(id)
        if not post:
            raise RepositoryNotFoundException("Post", id)
        return post

    def create(self, post: PostIn) -> Optional[Post]:
        if self.get_by_title(post.title):
            raise RepositoryAlreadyExistsException("Post", post.title)
        post_in_dict = post.model_dump()
        post_in_dict["id"] = self.increment_id_counter()
        post_model = Post(**post_in_dict)
        self.posts[post_model.id] = post_model
        return post_model

    def update(self, id: int, post: PostPut) -> Optional[Post]:
        stored_post = self.posts.get(id)
        if not stored_post:
            raise RepositoryNotFoundException("Post", id)

        # Actualizar los atributos del post existente
        update_data = post.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_post, key, value)

        return stored_post

    def delete(self, id: int) -> None:
        if not self.posts.get(id):
            raise RepositoryNotFoundException("Post", id)
        self.posts[id].soft_delete()

    def increment_id_counter(self) -> int:
        self.id_counter += 1
        return self.id_counter

    def get_by_title(self, title: str) -> Optional[Post]:
        return next((post for post in self.posts.values() if post.title == title), None)
