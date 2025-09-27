from pydantic import BaseModel, ConfigDict, Field

from api_security.core.enums.roles import UserRoles


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    id: int = Field(..., alias="sub")
    full_name: str
    username: str
    email: str
    role: UserRoles
    is_active: bool
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
