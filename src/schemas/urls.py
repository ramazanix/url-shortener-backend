from pydantic import UUID4, BaseModel, Field, validator
from datetime import datetime


class UrlSchemaBase(BaseModel):
    full_name: str
    short_name: str
    created_at: str

    @validator("created_at", pre=True)
    def parse_date(cls, value):
        return datetime.strftime(value, "%X %d.%m.%Y %Z")

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
    created_at: str
    user_id: UUID4

    @validator("created_at", pre=True)
    def parse_date(cls, value):
        return datetime.strftime(value, "%X %d.%m.%Y %Z")

    class Config:
        orm_mode = True
