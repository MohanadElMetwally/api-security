from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api_security.models.base import PkIntIdMixin
from api_security.models import Base


class Notes(Base, PkIntIdMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str]

    user = relationship("Users", back_populates="notes", lazy="selectin")
