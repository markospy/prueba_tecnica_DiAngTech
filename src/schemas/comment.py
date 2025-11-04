from datetime import datetime

from pydantic import BaseModel, Field

from schemas.user import UserForShowOut


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


class CommentIn(CommentBase):
    pass


class CommentPut(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


class CommentOut(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class CommentForPostOut(BaseModel):
    id: int
    user: UserForShowOut
    content: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
