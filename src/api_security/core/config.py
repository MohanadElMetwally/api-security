import secrets
from pathlib import Path
from typing import Final
from urllib.parse import urlencode

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from api_security.core.enums.backend import DatabaseBackend

API_SECURITY_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC_ROOT: Final[Path] = API_SECURITY_ROOT.parent
PROJECT_ROOT: Final[Path] = SRC_ROOT.parent


class Settings(BaseSettings):
    DEBUG: bool = False

    PROJECT_NAME: str = "APISecurity"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # +----------------+
    # |    Database    |
    # +----------------+

    DATABASE_PROVIDER: DatabaseBackend

    MSSQL_SERVER: str | None = None
    MSSQL_PORT: int | None = None
    MSSQL_USER: str | None = None
    MSSQL_PASSWORD: str | None = None
    MSSQL_DB: str | None = None
    MSSQL_DRIVER: str | None = None

    PSQL_USER: str | None = None
    PSQL_SERVER: str | None = None
    PSQL_PASSWORD: str | None = None
    PSQL_PORT: int | None = None
    PSQL_DB: str | None = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa: N802
        provider = self.DATABASE_PROVIDER

        ms_async_scheme = "mssql+aioodbc"
        pg_async_scheme = "postgresql+asyncpg"

        pg_query = {"command_timeout": 30, "ssl": "disable"}
        mss_query = {
            "driver": self.MSSQL_DRIVER,
            "TrustServerCertificate": "yes",
            "encrypt": "no",
            "timeout": 30,
            "command_timeout": 30,
        }

        db_config = {
            DatabaseBackend.MSSQL: {
                "scheme": ms_async_scheme,
                "host": self.MSSQL_SERVER,
                "port": self.MSSQL_PORT,
                "username": self.MSSQL_USER,
                "password": self.MSSQL_PASSWORD,
                "path": self.MSSQL_DB,
                "query": mss_query,
            },
            DatabaseBackend.PSQL: {
                "scheme": pg_async_scheme,
                "host": self.PSQL_SERVER,
                "port": self.PSQL_PORT,
                "username": self.PSQL_USER,
                "password": self.PSQL_PASSWORD,
                "path": self.PSQL_DB,
                "query": pg_query,
            },
        }

        connection = db_config[provider]

        connection.update({"query": urlencode(connection["query"])})
        return MultiHostUrl.build(**connection).unicode_string()

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env.dev",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()  # type: ignore
