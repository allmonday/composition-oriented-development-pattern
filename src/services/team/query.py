from .model import Team
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_teams(session: AsyncSession):
    return (await session.execute(select(Team))).scalars().all()