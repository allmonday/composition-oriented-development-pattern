from .model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import src.db as db
from pydantic2_resolve import build_object

async def batch_get_users_by_ids(session: AsyncSession, user_ids: list[int]):
    users = (await session.execute(select(User).where(User.id.in_(user_ids)))).scalars().all()
    return users

async def user_batch_loader(user_ids: list[int]):
    async with db.async_session() as session:
        users = await batch_get_users_by_ids(session, user_ids)
        return build_object(users, user_ids, lambda u: u.id)

