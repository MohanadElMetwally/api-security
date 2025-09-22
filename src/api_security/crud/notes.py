from sqlalchemy.ext.asyncio import AsyncSession

from api_security import models, schemas


async def create_note(session: AsyncSession, note_create: schemas.NoteCreate) -> None:
    note_data = note_create.model_dump()

    note = models.Notes(**note_data)
    session.add(note)
    await session.commit()
    await session.refresh(note)


async def update_note(
    session: AsyncSession, id: int, note_update: schemas.NoteUpdate
) -> models.Notes:
    note = await session.get(models.Notes, id)
    if not note:
        raise Exception(f"Note of ID: {id} was not found.")
    note_data = note_update.model_dump(exclude_unset=True)
    for field, value in note_data.items():
        if not hasattr(note, field):
            continue
        setattr(note, field, value)
    await session.commit()
    await session.refresh(note)
    return note
