from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from schemas.tags import TagForPostOut
from schemas.user import UserForShowOut


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=5000)
    tags: Optional[List[str]] = None


class PostIn(PostBase):
    pass


class PostPut(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1, max_length=5000)
    tags: Optional[List[str]] = None


class PostOut(PostBase):
    id: int
    user: UserForShowOut
    tags: Optional[List[TagForPostOut]] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
