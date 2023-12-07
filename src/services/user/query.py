from .model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_users(session: AsyncSession):
    users = (await session.execute(select(User))).scalars().all()
    return users