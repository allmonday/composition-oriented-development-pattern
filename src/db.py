from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .model import Base
import src.services.sprint.mock as sm
import src.services.story.mock as stm
import src.services.task.mock as tm
import src.services.team.mock as tem
import src.services.user.mock as um

engine = create_async_engine(
    "sqlite+aiosqlite://",
    echo=False,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def prepare():
    async with async_session() as session:
        async with session.begin():
            records = sm.sprints + stm.stories + tm.tasks + tem.team_users + tem.teams + um.users
            session.add_all(records)
