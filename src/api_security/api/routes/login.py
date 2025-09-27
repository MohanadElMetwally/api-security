from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from api_security import crud
from api_security.api.deps import SessionDep
from api_security.core import security
from api_security.core.config import settings
from api_security.core.exceptions.api.users import (
    UserNotActiveException,
    UserNotFoundException,
)
from api_security.schemas.base import Token

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
    session: SessionDep,
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await crud.users.authenticate(
        session, user_credentials.username, user_credentials.password
    )

    if not user:
        raise UserNotFoundException

    if not user.is_active:
        raise UserNotActiveException
    time_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=security.create_access_token(user, time_expire))
