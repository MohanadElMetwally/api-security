from pathlib import Path
from typing import Final
from urllib.parse import urlencode

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

API_SECURITY_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC_ROOT: Final[Path] = API_SECURITY_ROOT.parent
PROJECT_ROOT: Final[Path] = SRC_ROOT.parent

class Settings(BaseSettings):
    DEBUG: bool = False

    PROJECT_NAME: str = "APISecurity"
    API_V1_STR: str = "/api/v1"

    # +----------------+
    # |    Database    |
    # +----------------+

    MSSQL_SERVER: str | None = None
    MSSQL_PORT: int | None = None
    MSSQL_USER: str | None = None
    MSSQL_PASSWORD: str | None = None
    MSSQL_DB: str | None = None
    MSSQL_DRIVER: str | None = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa: N802
        ms_async_scheme = "mssql+aioodbc"

        connection = {
            "scheme": ms_async_scheme,
            "host": self.MSSQL_SERVER,
            "port": self.MSSQL_PORT,
            "username": self.MSSQL_USER,
            "password": self.MSSQL_PASSWORD,
            "path": self.MSSQL_DB,
            "query": {
                "driver": self.MSSQL_DRIVER,
                "TrustServerCertificate": "yes",
                "encrypt": "no",
                "timeout": 30,
                "command_timeout": 30,
            },
        }

        connection.update({"query": urlencode(connection["query"])})
        return MultiHostUrl.build(**connection).unicode_string()
    
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

settings = Settings()
