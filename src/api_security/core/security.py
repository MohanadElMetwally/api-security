from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext

from api_security.core.config import settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def create_access_token(sub: int, expire_mins: timedelta) -> str:
    expire = datetime.now(UTC) + expire_mins
    to_encode = {
        "exp": expire,
        "sub": str(sub),
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
