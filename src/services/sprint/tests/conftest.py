from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from src.services.sprint.mock import _sprints
from src.services.sprint.model import Sprint
import pytest
from src.db import Base


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

@pytest.fixture
async def session_factory(in_memory_db, create_db):
    sf = async_sessionmaker(bind=in_memory_db, expire_on_commit=False)
    async with sf() as session:
        session.add_all([Sprint(**s) for s in _sprints])
        await session.commit()
    yield sf

@pytest.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session
