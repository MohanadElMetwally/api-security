from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from api_security import crud
from api_security.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_super_user,
)
from api_security.models import Users
from api_security.schemas.base import Message
from api_security.schemas.users import UserCreate, UserPublic, UsersPublic, UserUpdate

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_super_user)],
    response_model=UsersPublic,
)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    stmt = select(Users).order_by(Users.id).offset(skip).limit(limit)
    users = (await session.execute(stmt)).scalars().all()

    return {"users": users}


@router.get("/me", response_model=UserPublic)
async def read_me(current_user: CurrentUser) -> Any:
    return current_user


@router.get("/{id}", response_model=UserPublic)
async def read_user(id: int, session: SessionDep) -> Any:
    user = await session.get(Users, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


@router.post("/", response_model=UserPublic)
async def create_user(session: SessionDep, user_create: UserCreate) -> Any:
    user = await crud.users.create_user(session, user_create)
    return user


@router.patch("/me")
async def update_me(
    session: SessionDep, current_user: CurrentUser, user_update: UserUpdate
) -> Message:
    await crud.users.update_user_me(session, current_user, user_update)
    return Message(message="Your information has been updated successfully!")


@router.patch("/{id}", dependencies=[Depends(get_current_active_super_user)])
async def update_user(id: int, session: SessionDep, user_update: UserUpdate) -> Message:
    await crud.users.update_user(session, id, user_update)
    return Message(message="User information has been updated successfully!")
