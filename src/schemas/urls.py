from pydantic import UUID4, BaseModel, Field, validator
from datetime import datetime


class UrlSchemaBase(BaseModel):
    full_name: str
    short_name: str

    class Config:
        orm_mode = True


class UrlSchemaCreateDefault(BaseModel):
    full_name: str = Field(max_length=150)


class UrlSchemaCreateCustom(UrlSchemaCreateDefault):
    short_name: str = Field(max_length=20)


class UrlSchemaUpdateCustom(BaseModel):
    short_name: str | None = Field(max_length=20)
    full_name: str | None = Field(max_length=150)


class UrlSchema(BaseModel):
    id: UUID4
    full_name: str
    short_name: str
    user_id: UUID4

    class Config:
        orm_mode = True
