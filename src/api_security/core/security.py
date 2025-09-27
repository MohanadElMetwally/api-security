from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext

from api_security.core.config import settings
from api_security.models.users import Users
from api_security.schemas.base import UserInfo

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def create_access_token(user: Users, expire_mins: timedelta) -> str:
    expire = datetime.now(UTC) + expire_mins
    jwt_subject = UserInfo.model_validate(user)
    to_encode = {
        "exp": expire,
        "sub": str(jwt_subject.id),
        **jwt_subject.model_dump(exclude={"id"})
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
