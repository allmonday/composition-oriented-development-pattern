from .model import Sprint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import src.db as db
from pydantic2_resolve import build_list

async def batch_get_sprint_by_ids(session: AsyncSession, team_ids: list[int]):
    users = (await session.execute(select(Sprint).where(Sprint.team_id.in_(team_ids)))).scalars().all()
    return users

async def team_to_sprint_loader(team_ids: list[int]):
    async with db.async_session() as session:
        sprints = await batch_get_sprint_by_ids(session, team_ids)
        return build_list(sprints, team_ids, lambda u: u.team_id)