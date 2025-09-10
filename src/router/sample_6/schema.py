from typing import Optional
from pydantic_resolve import Loader, ensure_subset, model_config
from pydantic import BaseModel, ConfigDict, Field
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

@ensure_subset(ts.Task)
@model_config()
class Sample6TaskDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    owner_id: int = Field(exclude=True)
    name: str
    def post_name(self):
        return 'task name: ' + self.name

    user: Optional[us.User] = None
    def resolve_user(self, loader=Loader(ul.user_batch_loader)):
        return loader.load(self.owner_id)

@ensure_subset(ss.Story)
@model_config()
class Sample6StoryDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(exclude=True)
    name: str
    def post_name(self):
        return 'story name: ' + self.name

    tasks: list[Sample6TaskDetail] = []
    def resolve_tasks(self, loader=Loader(tl.story_to_task_loader)):
        return loader.load(self.id)
    
@ensure_subset(sps.Sprint)  # pick what you want.
@model_config()
class Sample6SprintDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(exclude=True)
    name: str
    def post_name(self):
        return 'sprint name: ' + self.name

    stories: list[Sample6StoryDetail] = []
    def resolve_stories(self, loader=Loader(sl.sprint_to_story_loader)):
        return loader.load(self.id)

@ensure_subset(tms.Team)
@model_config()
class Sample6TeamDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(exclude=True)
    name: str
    def post_name(self):
        return 'team name: ' + self.name

    sprints: list[Sample6SprintDetail] = []
    def resolve_sprints(self, loader=Loader(spl.team_to_sprint_loader)):
        return loader.load(self.id)
    
class Sample6Root(BaseModel):
    summary: str
    teams: list[Sample6TeamDetail] = [] 
    async def resolve_teams(self):
        async with db.async_session() as session:
            teams = await tmq.get_teams(session)
            return teams