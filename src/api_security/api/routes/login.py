from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from api_security.api.deps import SessionDep
from api_security.schemas.base import Token

router = APIRouter()


@router.post("/access-token")
async def login_access_token(
    session: SessionDep,
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:...
