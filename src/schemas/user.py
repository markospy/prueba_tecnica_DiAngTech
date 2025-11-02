from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=30)
    fullname: str = Field(..., min_length=1, max_length=30)
    email: str = Field(..., min_length=1, max_length=30)


class UserIn(UserBase):
    password: str = Field(..., min_length=1, max_length=30)


class UserPut(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=30)
    fullname: str | None = Field(None, min_length=1, max_length=30)
    email: str | None = Field(None, min_length=1, max_length=30)
    password: str | None = Field(None, min_length=1, max_length=30)


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
