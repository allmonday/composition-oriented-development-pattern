from .model import Sprint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_sprints(session: AsyncSession):
    return (await session.execute(select(Sprint))).scalars().all()

async def get_sprints_by_ids(ids: list[int], session: AsyncSession):
    return (await session.execute(select(Sprint).where(Sprint.id.in_(ids)))).scalars().all()