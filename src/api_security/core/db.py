from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api_security.core.config import settings
from api_security.core.enums.backend import DatabaseBackend

connection_args = {"timeout": 30}

if settings.DATABASE_PROVIDER == DatabaseBackend.MSSQL:
    connection_args["autocommit"] = False

engine: AsyncEngine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    future=True,
    pool_recycle=3600,
    connect_args=connection_args,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
