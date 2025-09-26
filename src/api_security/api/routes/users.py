from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from api_security.api.deps import SessionDep
from api_security.models import Users
from api_security.schemas.users import UserPublic, UsersPublic

router = APIRouter()

@router.get("/", response_model=UsersPublic)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    stmt = select(Users).order_by(Users.id).offset(skip).limit(limit)
    users = (await session.execute(stmt)).scalars().all()

    return {"users": users}


@router.get("/{id}", response_model=UserPublic)
async def read_user(id: int, session: SessionDep) -> Any:
    user = await session.get(Users, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
