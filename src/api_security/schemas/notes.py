from pydantic import BaseModel, Field, computed_field


class NoteCreate(BaseModel):
    user_id: int
    content: str


class NoteUpdate(BaseModel):
    content: str


class NotePublic(BaseModel):
    id: int
    user_id: int
    content: str


class NotesPublic(BaseModel):
    notes: list[NotePublic] = Field(default_factory=list)

    @computed_field
    def count(self) -> int:
        return len(self.notes)
