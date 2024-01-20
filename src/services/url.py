from src.schemas.urls import (
    UrlSchemaCreateCustom,
    UrlSchemaCreateDefault,
    UrlSchemaUpdateCustom,
)
from src.utils import shortify_url
from src.models import Url
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select as sa_select
from sqlalchemy import update as sa_update


async def get_by_id(db: AsyncSession, url_id: UUID4) -> Url | None:
    return await db.get(Url, url_id)


async def get_by_short_name(db: AsyncSession, url_short_name: str) -> Url | None:
    return (
        await db.execute(sa_select(Url).where(Url.short_name == url_short_name))
    ).scalar_one_or_none()


async def create_default(
    db: AsyncSession, url: UrlSchemaCreateDefault, user_id: UUID4
) -> Url:
    short_name = shortify_url(url.full_name)
    db_url = Url(full_name=url.full_name, short_name=short_name, user_id=user_id)
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url


async def create_custom(
    db: AsyncSession, url: UrlSchemaCreateCustom, user_id: UUID4
) -> Url | None:
    if await get_by_short_name(db, url.short_name):
        return None

    db_url = Url(full_name=url.full_name, short_name=url.short_name, user_id=user_id)
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url


async def update_custom(
    db: AsyncSession, payload: UrlSchemaUpdateCustom, url: Url
) -> Url:
    update_data = payload.dict(exclude_none=True, exclude_unset=True)

    query = sa_update(Url).where(Url.id == url.id).values(update_data)
    await db.execute(query)
    await db.commit()
    await db.refresh(url)
    return url


async def delete(db: AsyncSession, url: Url) -> None:
    await db.delete(url)
    await db.commit()
