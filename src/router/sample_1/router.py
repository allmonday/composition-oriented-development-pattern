from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic2_resolve import Resolver
import src.db as db

import src.services.task.schema as ts
import src.services.user.schema as us

import src.services.user.query as uq
import src.services.story.query as sq
import src.services.sprint.query as spq

from .schema import Sample1TaskDetail, Sample1StoryDetail, Sample1SprintDetail

route = APIRouter(tags=['sample_1'], prefix="/sample_1")

@route.get('/users', response_model=List[us.User])
async def get_users(session: AsyncSession = Depends(db.get_session)):
    """
    1.1 
    return list of user
    """
    return await uq.get_users(session)


import src.services.task.query as tq
@route.get('/tasks', response_model=List[ts.Task])
async def get_tasks(session: AsyncSession = Depends(db.get_session)):
    """
    1.2
    return list of tasks
    """
    return await tq.get_tasks(session)


@route.get('/tasks-with-detail', response_model=List[Sample1TaskDetail])
async def get_tasks_with_detail(session: AsyncSession = Depends(db.get_session)):
    """
    1.3
    return list of tasks(user)
    """
    tasks = await tq.get_tasks(session)
    tasks = [Sample1TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver().resolve(tasks)
    return tasks


@route.get('/stories-with-detail', response_model=List[Sample1StoryDetail])
async def get_stories_with_detail(session: AsyncSession = Depends(db.get_session)):
    """
    1.4
    return list of story(task(user))
    """
    stories = await sq.get_stories(session)
    stories = [Sample1StoryDetail.model_validate(t) for t in stories]
    stories = await Resolver().resolve(stories)
    return stories


@route.get('/sprints-with-detail', response_model=List[Sample1SprintDetail])
async def get_sprints_with_detail(session: AsyncSession = Depends(db.get_session)):
    """
    1.5
    return list of sprint(story(task(user)))
    """
    sprints = await spq.get_sprints(session)
    sprints = [Sample1SprintDetail.model_validate(t) for t in sprints]
    sprints = await Resolver().resolve(sprints)
    return sprints