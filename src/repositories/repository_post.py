from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.models import Post
from repositories.exceptions import RepositoryAlreadyExistsException, RepositoryNotFoundException
from repositories.repository_base import RepositoryBase
from schemas.post import PostIn


class RepositoryPost(RepositoryBase):

    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self) -> Optional[List[Post]]:
        with self.session as session:
            return Post.all_active(session).all()

    def get_by_id(self, id: int) -> Optional[Post]:
        with self.session as session:
            return Post.get_by_id(session, id)

    def create(self, schema: PostIn) -> Optional[Post]:
        post = Post(**schema.model_dump())
        with self.session as session:
            try:
                session.add(post)
                session.commit()
                return post
            except IntegrityError:
                session.rollback()
                raise RepositoryAlreadyExistsException("Post", post.title)

    def update(self, id: int, schema: PostIn) -> Optional[Post]:
        with self.session as session:
            post: Post | None = Post.get_by_id(session, id)
            if not post:
                raise RepositoryNotFoundException("Post", id)
            stored_post_model = Post(**post.__dict__)
            update_post_data = schema.model_dump(exclude_unset=True)
            update_post = stored_post_model.model_copy(update=update_post_data)
            session.add(update_post)
            session.commit()
            return update_post

    def delete(self, id: int) -> None:
        with self.session as session:
            post = Post.get_by_id(session, id)
            if not post:
                raise RepositoryNotFoundException("Post", id)
            post.soft_delete()
            session.commit()
