from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.urls import UrlSchemaBase
from src.schemas.user import UserSchema, UserSchemaCreate, UserSchemaBase
from src.services.user import create, delete
from src.config import settings
from src.db import get_db
from src.dependencies import Auth, auth_checker
from src.redis import redis_conn


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me", response_model=UserSchema)
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    authorize: Annotated[Auth, Depends(auth_checker)],
):
    return await authorize.get_current_user(db)


@users_router.post("", response_model=UserSchema, status_code=201)
async def create_user(
    user: UserSchemaCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    new_user = await create(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return new_user


@users_router.delete("/me", status_code=204)
async def delete_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    authorize: Annotated[Auth, Depends(auth_checker)],
):
    current_user = await authorize.get_current_user(db)

    redis_conn.setex(authorize.jti, settings.AUTHJWT_REFRESH_TOKEN_EXPIRES, "true")
    return await delete(db, current_user)


@users_router.get("/me/urls", response_model=list[UrlSchemaBase])
async def get_current_user_urls(
    db: Annotated[AsyncSession, Depends(get_db)],
    authorize: Annotated[Auth, Depends(auth_checker)],
):
    current_user = await authorize.get_current_user(db)
    return current_user.urls
