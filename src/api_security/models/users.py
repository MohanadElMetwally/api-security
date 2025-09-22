from sqlalchemy.orm import Mapped, relationship

from api_security._typing.sqla import bit0, bit1
from api_security.models import Base
from api_security.models.base import PkIntIdMixin
from api_security.core.enums.roles import UserRoles

class Users(Base, PkIntIdMixin):
    full_name: Mapped[str]
    role: Mapped[UserRoles]
    hashed_password: Mapped[str]
    is_active: Mapped[bit1]
    is_deleted: Mapped[bit0]

    notes = relationship("Notes", back_populates="user", lazy="selectin")
