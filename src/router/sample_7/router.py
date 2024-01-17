from collections import defaultdict
from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic2_resolve import Resolver, build_list
import src.db as db
import src.services.user.query as uq
import src.services.story.query as sq
import src.services.sprint.query as spq
import src.services.team.query as tq
import src.services.task.query as tskq
from .schema import (
    SprintToStoryLoader,
    TeamToSprintLoader,
    UserLoader,
    Sample7TeamDetail,
    Sample7TaskDetail)

route = APIRouter(tags=['sample_7'], prefix="/sample_7")

def add_to_loader(loader, items, get_key):
    _map = defaultdict(list)
    for item in items:
        _map[get_key(item)].append(item)
    for k, v in _map.items():
        loader.prime(k, v)

def add_single_to_loader(loader, items, get_key):
    _map = {}
    for item in items:
        _map[get_key(item)] = item
    for k, v in _map.items():
        loader.prime(k, v)

@route.get('/tasks', response_model=list[Sample7TaskDetail])
async def get_tasks(session: AsyncSession = Depends(db.get_session)):
    users = await uq.get_users(session)
    user_loader = UserLoader()
    add_single_to_loader(user_loader, users, lambda u: u.id)

    tasks = await tskq.get_tasks(session)
    tasks = [Sample7TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver(loader_instances={UserLoader: user_loader}).resolve(tasks)
    return tasks


@route.get('/user/stat', response_model=list[Sample7TeamDetail])
async def get_user_stat(session: AsyncSession = Depends(db.get_session)):
    sprint_to_story_loader = SprintToStoryLoader()
    team_to_sprint_loader = TeamToSprintLoader()

    users = await uq.get_user_by_ids([1], session)
    stories = await sq.get_stories_by_owner_ids([u.id for u in users], session)
    add_to_loader(sprint_to_story_loader, stories, lambda s: s.sprint_id)

    sprint_ids = list({s.sprint_id for s in stories})
    sprints = await spq.get_sprints_by_ids(sprint_ids, session)
    add_to_loader(team_to_sprint_loader, sprints, lambda s: s.team_id)

    team_ids = list({s.team_id for s in sprints})

    teams = await tq.get_team_by_ids(team_ids, session)
    teams = [Sample7TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver(loader_instances={
        SprintToStoryLoader: sprint_to_story_loader,
        TeamToSprintLoader: team_to_sprint_loader
    }).resolve(teams)
    return teams

