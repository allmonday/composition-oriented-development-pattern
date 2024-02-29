from .model import Story
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import src.db as db
from pydantic_resolve import build_list

async def batch_get_stories_by_ids(session: AsyncSession, sprint_ids: list[int]):
    users = (await session.execute(select(Story).where(Story.sprint_id.in_(sprint_ids)))).scalars().all()
    return users

async def sprint_to_story_loader(sprint_ids: list[int]):
    async with db.async_session() as session:
        stories = await batch_get_stories_by_ids(session, sprint_ids)
        return build_list(stories, sprint_ids, lambda u: u.sprint_id)