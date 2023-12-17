from .model import Team
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_teams(session: AsyncSession):
    return (await session.execute(select(Team))).scalars().all()

async def get_team_by_id(session: AsyncSession, team_id: int):
    return (await session.execute(select(Team).where(Team.id == team_id))).scalar_one_or_none()

async def get_team_by_ids(team_ids: list[int], session: AsyncSession):
    return (await session.execute(select(Team).where(Team.id.in_(team_ids)))).scalars().all()