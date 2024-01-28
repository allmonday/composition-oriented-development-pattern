from typing import List, Optional
from pydantic2_resolve import LoaderDepend, ensure_subset
from pydantic import BaseModel, ConfigDict
import src.db as db

import src.services.task.loader as tl
import src.services.user.loader as ul
import src.services.story.loader as sl
import src.services.sprint.loader as spl

import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps
import src.services.team.schema as tms

import src.services.team.query as tmq

class Sample6TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)

class Sample6StoryDetail(ss.Story):
    tasks: list[Sample6TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)
    
@ensure_subset(sps.Sprint)  # pick what you want.
class Sample6SprintDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    team_id: int

    stories: list[Sample6StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

class Sample6TeamDetail(tms.Team):
    sprints: list[Sample6SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)
    
class Sample6Root(BaseModel):
    summary: str
    teams: list[Sample6TeamDetail] = [] 
    async def resolve_teams(self):
        async with db.async_session() as session:
            teams = await tmq.get_teams(session)
            return teams