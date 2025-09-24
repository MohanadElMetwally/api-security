from sqlalchemy.orm import Mapped, mapped_column, relationship

from api_security._typing.sqla import bit0, bit1, vstr, vstr255
from api_security.core.enums.roles import UserRoles
from api_security.models import Base
from api_security.models.base import PkIntIdMixin


class Users(Base, PkIntIdMixin):
    full_name: Mapped[vstr]
    role: Mapped[UserRoles]
    username: Mapped[vstr255] = mapped_column(unique=True)
    email: Mapped[vstr255] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bit1]
    is_deleted: Mapped[bit0]

    notes = relationship("Notes", back_populates="user", lazy="selectin")
