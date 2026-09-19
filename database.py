"""Async SQLite persistence for projects and daily copilot logs."""

from collections.abc import AsyncIterator
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()
load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", "sqlite+aiosqlite:///./finadvisor.db")
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provide an async session for the local SQLite database."""
    async with SessionLocal() as session:
        yield session
