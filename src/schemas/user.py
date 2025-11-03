from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


def password_strong(v):
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in v):
        raise ValueError("Password must contain uppercase")
    if not any(c.isdigit() for c in v):
        raise ValueError("Password must contain digit")
    return v


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    fullname: str = Field(..., min_length=5, max_length=30)
    email: EmailStr | None = None
    bio: str | None = Field(None, min_length=1, max_length=500)
    avatar: str | None = Field(None, min_length=1, max_length=200)

    @field_validator("username")
    def username_alphanumeric(cls, v):
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return v


class UserIn(UserBase):
    password: str = Field(..., min_length=1, max_length=128)

    @field_validator("password")
    def validate_password(cls, v):
        return password_strong(v)


class UserPut(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=30)
    fullname: str | None = Field(None, min_length=5, max_length=30)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=128)
    bio: str | None = Field(None, min_length=1, max_length=500)
    avatar: str | None = Field(None, min_length=1, max_length=200)

    @field_validator("password")
    def validate_password(cls, v):
        return password_strong(v)


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
