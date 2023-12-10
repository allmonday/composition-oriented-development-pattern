from .model import Task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import src.db as db
from pydantic2_resolve import build_list

async def batch_get_tasks_by_ids(session: AsyncSession, story_ids: list[int]):
    users = (await session.execute(select(Task).where(Task.story_id.in_(story_ids)))).scalars().all()
    return users

async def story_to_task_loader(story_ids: list[int]):
    async with db.async_session() as session:
        tasks = await batch_get_tasks_by_ids(session, story_ids)
        return build_list(tasks, story_ids, lambda u: u.story_id)