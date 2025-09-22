from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_security.core.db import get_db


async def get_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_db() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session_dep)]
