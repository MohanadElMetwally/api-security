from sqlalchemy.orm import Mapped, mapped_column


class PkIntIdMixin:
    """Primary key auto-incremental integer id mixin."""

    id: Mapped[int] = mapped_column(
        nullable=False, primary_key=True, autoincrement=True
    )
