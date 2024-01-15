from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
import pytest
from src.db import Base

# common
@pytest.fixture(scope="session")
async def in_memory_db():
    return create_async_engine('sqlite+aiosqlite:///:memory:')

@pytest.fixture
async def create_db(in_memory_db: AsyncEngine):
    async with in_memory_db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with in_memory_db.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)