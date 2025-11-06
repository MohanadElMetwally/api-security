from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_security import models, schemas
from api_security.core.security import get_hashed_password, verify_hashed_password
from api_security.models.users import Users


async def create_user(
    session: AsyncSession, user_create: schemas.UserCreate
) -> models.Users:
    user_data = user_create.model_dump(exclude={"password"})
    user_data["hashed_password"] = get_hashed_password(user_create.password)

    user = models.Users(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(
    session: AsyncSession, username: str
) -> models.Users | None:
    stmt = select(models.Users).where(models.Users.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(session: AsyncSession, email: str) -> models.Users | None:
    stmt = select(models.Users).where(models.Users.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def authenticate(
    session: AsyncSession, login: str, password: str
) -> models.Users | None:
    stmt = select(models.Users).where(
        or_(models.Users.username == login, models.Users.email == login)
    )
    user = (await session.execute(stmt)).scalars().first()
    if not user:
        return None
    return user if verify_hashed_password(password, user.hashed_password) else None


async def update_user(
    session: AsyncSession, id: int, user_update: schemas.UserUpdate
) -> models.Users:
    user = await session.get(Users, id)
    if not user:
        raise ValueError(f"User with id: {id} not found")
    user_data = user_update.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        if not hasattr(user, field):
            continue
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_me(
    session: AsyncSession, user_obj: Users, user_update: schemas.UserUpdate
) -> models.Users:
    user = user_obj
    user_data = user_update.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        if not hasattr(user, field):
            continue
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user
