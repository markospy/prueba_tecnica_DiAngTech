from datetime import datetime

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)


class TagIn(TagBase):
    pass


class TagPut(TagBase):
    pass


class TagOut(TagBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class TagForPostOut(TagBase):
    id: int
    name: str
