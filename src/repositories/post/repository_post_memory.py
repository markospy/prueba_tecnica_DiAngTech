from typing import List, Optional

from models.models import Post
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class RepositoryPostMemory(RepositoryBase):
    def __init__(self, posts: dict[int, Post] = {}, session=None):
        super().__init__(session=session)
        self.posts: dict[int, Post] = posts
        self.id_counter = 0

    async def get_all(self) -> Optional[List[Post]]:
        return list(self.posts.values())

    async def get_by_id(self, id: int) -> Optional[Post]:
        post = self.posts.get(id)
        if not post:
            raise RepositoryNotFoundException(entity_name="Post", id=id)
        return post

    async def create(self, post: PostIn) -> Optional[Post]:
        existing_post = await self.get_by_title(post.title)
        if existing_post:
            raise RepositoryAlreadyExistsException(entity_name="Post", name=post.title)
        post_in_dict = post.model_dump()
        post_in_dict["id"] = self.increment_id_counter()
        post_model = Post(**post_in_dict)
        self.posts[post_model.id] = post_model
        return post_model

    async def update(self, id: int, post: PostPut) -> Optional[Post]:
        stored_post = self.posts.get(id)
        if not stored_post:
            raise RepositoryNotFoundException(entity_name="Post", id=id)

        # Actualizar los atributos del post existente
        update_data = post.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stored_post, key, value)

        return stored_post

    async def delete(self, id: int) -> None:
        if not self.posts.get(id):
            raise RepositoryNotFoundException(entity_name="Post", id=id)
        self.posts[id].soft_delete()

    def increment_id_counter(self) -> int:
        self.id_counter += 1
        return self.id_counter

    async def get_by_title(self, title: str) -> Optional[Post]:
        return next((post for post in self.posts.values() if post.title == title), None)
