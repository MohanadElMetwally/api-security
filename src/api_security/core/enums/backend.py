from enum import StrEnum, auto


class DatabaseBackend(StrEnum):
    PSQL = auto()
    MSSQL = auto()
