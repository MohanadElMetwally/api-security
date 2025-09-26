from sqlalchemy.ext.asyncio import AsyncSession

from api_security import models, schemas


async def create_note(
    session: AsyncSession, id: int, note_create: schemas.NoteCreatePublic
) -> models.Notes:
    note_data = schemas.NoteCreate.model_validate(
        {**note_create.model_dump(), "user_id": id}
    )

    note = models.Notes(**note_data.model_dump())
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


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
