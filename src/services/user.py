from src.models import User
from src.schemas.user import UserSchemaCreate
from src.security import get_password_hash, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select as sa_select
from sqlalchemy.exc import NoResultFound


async def get_by_id(db: AsyncSession, user_id: str) -> User | None:
    return await db.get(User, user_id)


async def get_by_username(db: AsyncSession, username: str) -> User | None:
    return (
        await db.execute(sa_select(User).where(User.username == username))
    ).scalar_one_or_none()


async def get_with_paswd(db: AsyncSession, user: UserSchemaCreate) -> User | None:
    try:
        db_user = (
            await db.execute(sa_select(User).where((User.username == user.username)))
        ).scalar()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise NoResultFound
        return db_user
    except NoResultFound:
        return None


async def create(db: AsyncSession, user: UserSchemaCreate) -> User | None:
    if await get_by_username(db, user.username):
        return None

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
