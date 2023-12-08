from .model import Sprint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_sprints(session: AsyncSession):
    return (await session.execute(select(Sprint))).scalars().all()