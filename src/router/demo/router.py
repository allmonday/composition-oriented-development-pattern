from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic_resolve import Resolver
import src.db as db

import src.services.story.query as sq

from .schema import Story
from .schema1 import Story1
from .schema2 import Story2
from .schema3 import Story3

route = APIRouter(tags=['demo'], prefix="/demo")

@route.get('/stories', response_model=List[Story])
async def get_stories_with_detail(session: AsyncSession = Depends(db.get_session)):
    stories = await sq.get_stories(session)
    stories = [Story.model_validate(t) for t in stories]
    stories = await Resolver().resolve(stories)
    return stories

@route.get('/stories-1', response_model=List[Story1])
async def get_stories_with_detail_1(session: AsyncSession = Depends(db.get_session)):
    stories = await sq.get_stories(session)
    stories = [Story1.model_validate(t) for t in stories]
    stories = await Resolver().resolve(stories)
    return stories

@route.get('/stories-2', response_model=List[Story2])
async def get_stories_with_detail_2(session: AsyncSession = Depends(db.get_session)):
    stories = await sq.get_stories(session)
    stories = [Story2.model_validate(t) for t in stories]
    stories = await Resolver().resolve(stories)
    return stories

@route.get('/stories-3', response_model=List[Story3])
async def get_stories_with_detail_3(session: AsyncSession = Depends(db.get_session)):
    stories = await sq.get_stories(session)
    stories = [Story3.model_validate(t) for t in stories]
    stories = await Resolver().resolve(stories)
    return stories