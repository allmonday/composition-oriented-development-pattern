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
from .schema import SprintToStoryLoader, TeamToSprintLoader, Sample7TeamDetail

route = APIRouter(tags=['sample_7'], prefix="/sample_7")

@route.get('/user/stat', response_model=list[Sample7TeamDetail])
async def get_user_stat(session: AsyncSession = Depends(db.get_session)):
    sprintToStoryLoader = SprintToStoryLoader()
    teamToSprintLoader = TeamToSprintLoader()

    users = await uq.get_user_by_ids([1], session)
    stories = await sq.get_stories_by_owner_ids([u.id for u in users], session)
    sprint_ids = list({s.sprint_id for s in stories})

    # need better solution
    for _sprint_id, _stories in zip(sprint_ids, build_list(stories, sprint_ids, lambda s: s.sprint_id)):
        sprintToStoryLoader.prime(_sprint_id, _stories)

    sprints = await spq.get_sprints_by_ids(sprint_ids, session)
    team_ids = list({s.team_id for s in sprints})

    # need better solution
    for _team_id, _sprints in zip(team_ids, build_list(sprints, team_ids, lambda s: s.team_id)):
        teamToSprintLoader.prime(_team_id, _sprints)

    teams = await tq.get_team_by_ids(team_ids, session)
    print(teams)

    teams = [Sample7TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver(loader_instances={
        SprintToStoryLoader: sprintToStoryLoader,
        TeamToSprintLoader: teamToSprintLoader
    }).resolve(teams)
    return teams

