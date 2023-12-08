from .model import Story
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_stories(session: AsyncSession):
    users = (await session.execute(select(Story))).scalars().all()
    return users