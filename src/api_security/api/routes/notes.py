from typing import Any

from fastapi import APIRouter
from sqlalchemy import select

from api_security import crud
from api_security.api.deps import CurrentUser, SessionDep
from api_security.core.exceptions.api.notes import NoteNotFoundException
from api_security.models.notes import Notes
from api_security.schemas.base import Message
from api_security.schemas.notes import (
    NoteCreatePublic,
    NotePublic,
    NotesPublic,
    NoteUpdate,
)

router = APIRouter()


@router.get("/me", response_model=NotesPublic)
async def read_my_notes(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    stmt = (
        select(Notes)
        .where(Notes.user_id == current_user.id)
        .order_by(Notes.id)
        .offset(skip)
        .limit(limit)
    )
    notes = (await session.execute(stmt)).scalars().all()
    return {"notes": notes}


@router.get("/{id}", response_model=NotePublic)
async def read_note(id: int, current_user: CurrentUser, session: SessionDep) -> Any:
    note = await session.get(Notes, id)
    if not note or (note.user_id != current_user.id):
        raise NoteNotFoundException
    return note


@router.post("/", response_model=NotePublic)
async def create_note(
    session: SessionDep, current_user: CurrentUser, note_create: NoteCreatePublic
) -> Any:
    note = await crud.notes.create_note(session, current_user.id, note_create)
    return note


@router.patch("/{id}")
async def update_note(id: int, session: SessionDep, note_update: NoteUpdate) -> Message:
    await crud.notes.update_note(session, id, note_update)
    return Message(message="Note has been updated successfully!")
