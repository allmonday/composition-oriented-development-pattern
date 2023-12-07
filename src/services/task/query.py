from .model import Task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_tasks(session: AsyncSession):
    tasks = (await session.execute(select(Task))).scalars().all()
    return tasks