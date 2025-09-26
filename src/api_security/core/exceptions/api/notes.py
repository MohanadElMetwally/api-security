from fastapi import HTTPException, status


class NoteException(HTTPException):
    """Base exception for note-related errors."""

    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str | None = None,
        *,
        note_id: int | None = None,
        problem: str | None = "error occurred",
    ) -> None:
        """Initialize a NoteException."""
        identity: str = ""

        if note_id:
            identity = f" with id: {note_id}"

        detail = detail or f"Note{identity} {problem}"
        super().__init__(status_code=status_code, detail=detail)


class NoteNotFoundException(NoteException):
    """Raised when the requested note is not found in the database."""

    def __init__(
        self,
        note_id: int | None = None,
        detail: str | None = None,
        status_code: int = status.HTTP_404_NOT_FOUND,
        problem: str | None = "is not found",
    ) -> None:
        """Initialize a NoteNotFoundException."""
        super().__init__(
            status_code=status_code,
            detail=detail,
            note_id=note_id,
            problem=problem,
        )
