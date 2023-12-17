from .model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_users(session: AsyncSession):
    return (await session.execute(select(User))).scalars().all()

async def get_user_by_ids(ids: list[int], session: AsyncSession):
    return (await session.execute(select(User).where(User.id.in_(ids)))).scalars().all()
