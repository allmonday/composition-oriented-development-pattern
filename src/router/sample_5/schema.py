from typing import List, Optional
from pydantic2_resolve import LoaderDepend
from pydantic import BaseModel
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

class Sample5TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)

class Sample5StoryDetail(ss.Story):
    tasks: list[Sample5TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)
    
    task_count: int = 0
    def post_task_count(self):
        return len(self.tasks)
    
class Sample5SprintDetail(sps.Sprint):
    stories: list[Sample5StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.stories])

class Sample5TeamDetail(tms.Team):
    sprints: list[Sample5SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])
    
    description: str = ''
    def post_default_handler(self):
        self.description = f'team: "{self.name}" has {self.task_count} tasks in total.' 

    
class Sample5Root(BaseModel):
    summary: str
    team: Optional[Sample5TeamDetail] = None 
    async def resolve_team(self, context):
        async with db.async_session() as session:
            team_id = context['team_id']
            team = await tmq.get_team_by_id(session, team_id)
            return team