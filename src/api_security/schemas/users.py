from pydantic import BaseModel, Field, computed_field, field_validator

from api_security.core.enums.roles import UserRoles


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    role: UserRoles

    @field_validator("username")
    @classmethod
    def username_to_lower(cls, v: str) -> str:
        return v.lower()


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRoles | None = None
    password: str | None = None
    is_active: bool | None = None
    is_deleted: bool | None = None


class UserPublic(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    role: UserRoles
    is_active: bool
    is_deleted: bool


class UsersPublic(BaseModel):
    users: list[UserPublic] = Field(default_factory=list)

    @computed_field
    def count(self) -> int:
        return len(self.users)
