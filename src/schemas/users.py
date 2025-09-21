from pydantic import BaseModel, Field, computed_field

from src.core.enums.roles import UserRoles


class UserCreate(BaseModel):
    full_name: str
    password: str
    role: UserRoles


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRoles | None = None
    password: str | None = None
    is_active: bool | None = None
    is_deleted: bool | None = None


class UserPublic(BaseModel):
    id: int
    full_name: str
    role: UserRoles
    is_active: bool
    is_deleted: bool


class UsersPublic(BaseModel):
    users: list[UserPublic] = Field(default_factory=list)

    @computed_field
    def count(self):
        return len(self.users)
