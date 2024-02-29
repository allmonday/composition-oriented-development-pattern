from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic_resolve import Resolver
import src.db as db
from .schema import Sample6Root

route = APIRouter(tags=['sample_6'], prefix="/sample_6")

@route.get('/page-info', response_model=Sample6Root)
async def get_page_info(session: AsyncSession = Depends(db.get_session)):
    page = Sample6Root(summary="hello world")
    page = await Resolver().resolve(page)
    return page