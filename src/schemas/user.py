from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=30)
    fullname: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    bio: str | None = Field(None, min_length=1, max_length=500)
    avatar: str | None = Field(None, min_length=1, max_length=200)

    @field_validator("username")
    def username_alphanumeric(cls, v):
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return v


class UserIn(UserBase):
    password: str = Field(..., min_length=1, max_length=30)


class UserPut(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=30)
    fullname: str | None = Field(None, min_length=1, max_length=30)
    email: str | None = Field(None, min_length=1, max_length=30)
    password: str | None = Field(None, min_length=1, max_length=30)
    bio: str | None = Field(None, min_length=1, max_length=500)
    avatar: str | None = Field(None, min_length=1, max_length=200)


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class UserForShowOut(BaseModel):
    id: int
    username: str
    fullname: str
    avatar: str | None = None
