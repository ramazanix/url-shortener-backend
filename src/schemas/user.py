from pydantic import UUID4, BaseModel, Field, validator
from datetime import datetime
from .urls import UrlSchemaBase


class UserSchemaBase(BaseModel):
    username: str


class UserSchemaCreate(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=8, max_length=32)


class UserSchema(BaseModel):
    id: UUID4
    username: str
    created_at: str

    @validator("created_at", pre=True)
    def parse_date(cls, value):
        return datetime.strftime(value, "%X %d.%m.%Y %Z")

    class Config:
        orm_mode = True
