from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.models import Post
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn, PostPut


class RepositoryPostPostgres(RepositoryBase):

    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self) -> Optional[List[Post]]:
        return Post.all_active(self.session).all()

    def get_by_id(self, id: int) -> Optional[Post]:
        return Post.get_by_id(self.session, id)

    def create(self, schema: PostIn) -> Optional[Post]:
        post = Post(**schema.model_dump())
        try:
            self.session.add(post)
            self.session.commit()
            self.session.refresh(post)
            return post
        except IntegrityError:
            self.session.rollback()
            raise RepositoryAlreadyExistsException("Post", post.title)

    def update(self, id: int, schema: PostPut) -> Optional[Post]:
        post: Post | None = Post.get_by_id(self.session, id)
        if not post:
            raise RepositoryNotFoundException("Post", id)
        update_post_data = schema.model_dump(exclude_unset=True)
        update_post = post.model_copy(update=update_post_data)
        self.session.add(update_post)
        self.session.commit()
        self.session.refresh(update_post)
        return update_post

    def delete(self, id: int) -> None:
        post = Post.get_by_id(self.session, id)
        if not post:
            raise RepositoryNotFoundException("Post", id)
        post.soft_delete()
        self.session.commit()
