from datetime import datetime

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=5000)


class PostIn(PostBase):
    user_id: int


class PostPut(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1, max_length=5000)


class PostOut(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
