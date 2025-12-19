from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ThoughtBase(BaseModel):  # ----- PYDANTIC MODEL
    title: str
    content: str
    published: bool = True
    created_at: datetime


class CreateThought(BaseModel):
    title: str
    content: str
    published: bool = True


class UpdateThought(CreateThought):
    pass
