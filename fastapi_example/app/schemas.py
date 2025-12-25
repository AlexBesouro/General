from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID


# class ThoughtBase(BaseModel):  # ----- PYDANTIC MODEL
#     # user_id: UUID
#     title: str
#     content: str
#     published: bool = True
#     created_at: datetime


class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3, max_length=20)

    # EXTRA SECURITY TO VALIDATE PASSWORD
    # @field_validator("password")
    # def validate_password(cls, v: str) -> str:
    #     if len(v) < 8:
    #         raise ValueError("Password must be at least 8 characters long")

    #     if not any(c.isupper() for c in v):
    #         raise ValueError("Password must contain an uppercase letter")

    #     if not any(c.islower() for c in v):
    #         raise ValueError("Password must contain a lowercase letter")

    #     if not any(c.isdigit() for c in v):
    #         raise ValueError("Password must contain a number")

    #     if not any(c in "!@#$%^&*()-_=+[]{};:,.<>/?" for c in v):
    #         raise ValueError("Password must contain a special character")

    #     return v


class CreateUserResponse(BaseModel):
    email: EmailStr
    id: UUID
    created_at: datetime
    model_config = {
        "from_attributes": True
    }


class CreateThought(BaseModel):
    title: str
    content: str
    published: bool = True


class CreateThoughtResponse(CreateThought):
    user_id: UUID
    owner: CreateUserResponse


class UpdateThought(CreateThought):
    pass


# class LoginUser(BaseModel):
#     email: EmailStr
#     password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
