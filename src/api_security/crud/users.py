from sqlalchemy.ext.asyncio import AsyncSession

from api_security import models, schemas
from api_security.core.security import get_hashed_password


async def create_user(session: AsyncSession, user_create: schemas.UserCreate) -> None:
    user_data = user_create.model_dump(exclude={"password"})
    user_data["hashed_password"] = get_hashed_password(user_create.password)

    user = models.Users(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def update_user(
    session: AsyncSession, id: int, user_update: schemas.UserUpdate
) -> models.Users:
    user = await session.get(models.Users, id)
    if not user:
        raise Exception(f"User of ID: {id} was not found.")
    user_data = user_update.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        if not hasattr(user, field):
            continue
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user
