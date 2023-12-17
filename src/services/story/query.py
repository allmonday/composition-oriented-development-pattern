from .model import Story
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_stories(session: AsyncSession):
    return (await session.execute(select(Story))).scalars().all()

async def get_stories_by_owner_ids(ids: list[int], session: AsyncSession):
    return (await session.execute(select(Story)
                                  .where(Story.owner_id.in_(ids)))).scalars().all()