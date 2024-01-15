from sqlalchemy.ext.asyncio import async_sessionmaker
from src.services.sprint.mock import _sprints
from src.services.sprint.model import Sprint
import pytest

# service specific
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
