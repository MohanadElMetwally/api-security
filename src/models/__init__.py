import datetime as dt
import types
from collections.abc import Mapping
from enum import Enum
from types import MappingProxyType
from typing import (
    Any,
    Final,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from sqlalchemy import CheckConstraint, MetaData
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, declared_attr, registry
from sqlalchemy.types import BIGINT

from src.utils.serialization import to_snakecase

NAMING_CONVENTIONS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "df": "df_%(table_name)s_%(column0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
mapper_registry = registry(metadata=MetaData(naming_convention=NAMING_CONVENTIONS))


@mapper_registry.as_declarative_base()
class Base:
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # noqa
        return to_snakecase(cls.__name__)  # type: ignore

    type_annotation_map = {  # noqa
        int: BIGINT,
        dt.datetime: DATETIME2,
        Enum: lambda cls: SQLAEnum(
            cls,
            native_enum=False,
            check_constraint=True,
            validate_strings=True,
        ),
    }

    @declared_attr  # type: ignore
    def __table_args__(cls) -> tuple[Any, ...]:  # noqa
        """Generate check constraints for enum fields automatically."""
        constraints = []

        hints = get_type_hints(cls, include_extras=True)

        for attr_name, hint_type in hints.items():
            if get_origin(hint_type) is not Mapped:
                continue

            inner_type = get_args(hint_type)[0]

            if get_origin(inner_type) in (Union, types.UnionType):
                inner_args = get_args(inner_type)
                for arg in inner_args:
                    if arg is not type(None):
                        inner_type = arg
                        break

            if isinstance(inner_type, type) and issubclass(inner_type, Enum):
                constraint = CheckConstraint(
                    f"{attr_name} IN {tuple(c.value for c in inner_type)}",
                    name=f"ck_{cls.__tablename__}_{attr_name}_enum",
                )
                constraints.append(constraint)

        existing_args = getattr(cls, "__orig_table_args__", ())
        if isinstance(existing_args, dict):
            return (*constraints, existing_args)

        return (*existing_args, *constraints)
