from collections.abc import AsyncGenerator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api_security.core import security
from api_security.core.config import settings
from api_security.core.db import get_db
from api_security.core.enums.roles import UserRoles
from api_security.core.exceptions.api.users import (
    UserLackPrivilegesException,
    UserNotActiveException,
)
from api_security.schemas.base import TokenPayload, UserInfo

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth)]


async def get_session_dep() -> AsyncGenerator[AsyncSession, None]:
    async with get_db() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session_dep)]


async def get_active_current_user(token: TokenDep) -> UserInfo:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [security.ALGORITHM])
        _ = TokenPayload(**payload)
    except (ValidationError, InvalidTokenError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials: {e}",
        ) from e

    user = UserInfo(**payload)
    if not user.is_active:
        raise UserNotActiveException

    return user


CurrentUser = Annotated[UserInfo, Depends(get_active_current_user)]


async def get_current_active_super_user(current_user: CurrentUser) -> UserInfo:
    if current_user.role != UserRoles.SUPERUSER:
        raise UserLackPrivilegesException

    return current_user
