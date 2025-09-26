from fastapi import HTTPException, status


class UserException(HTTPException):
    """Base exception for user-related errors."""

    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str | None = None,
        *,
        user_id: int | None = None,
        user_email: str | None = None,
        problem: str | None = "error occurred",
    ) -> None:
        """Initialize a UserException."""
        if user_id and user_email:
            raise ValueError(
                "Set only one identity as the parameter either user_id or "
                "user_email, both cannot be set"
            )

        identity: str = ""

        if user_id:
            identity = f" with id: {user_id}"

        if user_email:
            identity = f" with email: {user_email}"

        detail = detail or f"User{identity} {problem}"
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(UserException):
    """Raised when the requested user is not found in the database."""

    def __init__(
        self,
        user_id: int | None = None,
        detail: str | None = None,
        status_code: int = status.HTTP_404_NOT_FOUND,
        problem: str | None = "is not found",
    ) -> None:
        """Initialize a UserNotFoundException."""
        super().__init__(
            status_code=status_code,
            detail=detail,
            user_id=user_id,
            problem=problem,
        )


class UserNotActiveException(UserException):
    """Raised when the requested user is found in the database but deactivated."""

    def __init__(
        self,
        user_id: int | None = None,
        user_email: str | None = None,
        detail: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        problem: str | None = "is not active",
    ) -> None:
        """Initialize a UserNotActiveException."""
        super().__init__(
            status_code=status_code,
            detail=detail,
            user_id=user_id,
            user_email=user_email,
            problem=problem,
        )


class UserAlreadyExistsException(UserException):
    """Raised when creating a user with the same email of another existing user."""

    def __init__(
        self,
        user_email: str | None = None,
        detail: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        problem: str | None = "already exists",
    ) -> None:
        """Initialize a UserAlreadyExistsException."""
        super().__init__(
            status_code=status_code,
            detail=detail,
            user_email=user_email,
            problem=problem,
        )


class UserWrongCredentialsException(UserException):
    def __init__(
        self,
        user_email: str | None = None,
        detail: str | None = "Incorrect username or password",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        problem: str | None = None,
    ) -> None:
        """Initialize a UserWrongCredentialsException."""
        super().__init__(
            status_code=status_code,
            detail=detail,
            user_email=user_email,
            problem=problem,
        )


class UserLackPrivilegesException(UserException):
    def __init__(
        self,
        user_email: str | None = None,
        detail: str | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
        problem: str
        | None = "does not have enough privileges to proceed with this request",
    ) -> None:
        """Initialize a UserLackPrivilegesException."""
        super().__init__(
            status_code=status_code,
            detail=detail,
            user_email=user_email,
            problem=problem,
        )
