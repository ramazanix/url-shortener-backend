from typing import Annotated
from validators import url as is_valid_url
from validators import slug as is_valud_slug
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.urls import (
    UrlSchemaBase,
    UrlSchemaCreateCustom,
    UrlSchemaUpdateCustom,
    UrlSchemaCreateDefault,
    UrlSchema,
)
from src.db import get_db
from src.dependencies import Auth, auth_checker
from src.services.url import (
    create_default,
    create_custom,
    update_custom,
    get_by_short_name,
    delete,
)


urls_router = APIRouter(prefix="/urls", tags=["Urls"])


@urls_router.post("/default", response_model=UrlSchema, status_code=201)
async def create_url_default(
    url: UrlSchemaCreateDefault,
    db: Annotated[AsyncSession, Depends(get_db)],
    authorize: Annotated[Auth, Depends(auth_checker)],
):
    if not is_valid_url(url.full_name):
        raise HTTPException(status_code=400, detail="Not valid url")

    current_user = await authorize.get_current_user(db)
    return await create_default(db, url, current_user.id)


@urls_router.post("/custom", response_model=UrlSchema, status_code=201)
async def create_url_custom(
    url: UrlSchemaCreateCustom,
    db: Annotated[AsyncSession, Depends(get_db)],
    authorize: Annotated[Auth, Depends(auth_checker)],
):
    if not is_valid_url(url.full_name):
        raise HTTPException(status_code=400, detail="Not valid url")

    if not is_valud_slug(url.short_name):
        raise HTTPException(status_code=400, detail="Not valid slug")

    current_user = await authorize.get_current_user(db)
    new_custom_url = await create_custom(db, url, current_user.id)

    if not new_custom_url:
        raise HTTPException(status_code=400, detail="Slug already in use")

    return new_custom_url


@urls_router.patch("/{short_name}", response_model=UrlSchema)
async def update_url(
    short_name: str,
    payload: UrlSchemaUpdateCustom,
    db: Annotated[AsyncSession, Depends(get_db)],
    authorize: Annotated[Auth, Depends(auth_checker)],
):
    existed_custom_url = await get_by_short_name(db, short_name)

    if not existed_custom_url:
        raise HTTPException(status_code=400, detail="Url not found")

    new_url_data: dict = payload.dict()
    if not any(new_url_data.values()):
        raise HTTPException(status_code=400)

    if new_url_data.get("short_name") and short_name != payload.short_name:
        another_url = await get_by_short_name(db, payload.short_name)

        if another_url:
            raise HTTPException(status_code=400, detail="Url occupied")

        if not is_valud_slug(payload.short_name):
            raise HTTPException(status_code=400, detail="Not valid slug")

    if (
        new_url_data.get("full_name")
        and existed_custom_url.full_name != payload.full_name
    ):
        if not is_valid_url(payload.full_name):
            raise HTTPException(status_code=400, detail="Not valid url")

    return await update_custom(db, payload, existed_custom_url)


@urls_router.delete("/{short_name}", status_code=204)
async def delete_url(
    short_name: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    autorize: Annotated[Auth, Depends(auth_checker)],
):
    db_url = await get_by_short_name(db, short_name)
    if not db_url:
        raise HTTPException(status_code=400, detail="Url not found")

    current_user = await autorize.get_current_user(db)
    if db_url.user_id != current_user.id:
        raise HTTPException(status_code=403)

    return await delete(db, db_url)


@urls_router.get("/{short_name}", response_model=UrlSchemaBase)
async def get_full_name(short_name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    url = await get_by_short_name(db, short_name)
    if not url:
        raise HTTPException(status_code=400, detail="Url not found")

    return url
