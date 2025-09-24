import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from api_security import crud, schemas
from api_security.core.db import engine, get_db
from api_security.core.enums.roles import UserRoles

PASS = "12345678"


async def init_users(session: AsyncSession) -> None:
    users = [
        {
            "full_name": "MohanadElMetwally",
            "username": "Honda",
            "email": "honda@gmail.com",
            "password": PASS,
            "role": UserRoles.SUPERUSER,
        },
        {
            "full_name": "BasyoneAbdElSalam",
            "username": "Basyone",
            "email": "basyone@gmail.com",
            "password": PASS,
            "role": UserRoles.USER,
        },
    ]
    for user in users:
        user_data = schemas.UserCreate.model_validate(user)
        await crud.users.create_user(session, user_data)


async def main() -> None:
    async with get_db() as session:
        try:
            await init_users(session)
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
