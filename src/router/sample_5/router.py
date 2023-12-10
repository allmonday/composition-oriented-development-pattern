from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic2_resolve import Resolver
import src.db as db
from .schema import Sample5Root
import src.services.team.query as tmq
import src.services.user.loader as ul

route = APIRouter(tags=['sample_5'], prefix="/sample_5")

@route.get('/page-info', response_model=Sample5Root)
async def get_page_info(session: AsyncSession = Depends(db.get_session)):
    page = Sample5Root(summary="hello world")
    page = await Resolver().resolve(page)
    return page