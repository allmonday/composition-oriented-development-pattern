from __future__ import annotations

from typing import Optional, Annotated
from pydantic_resolve import ICollector, LoadBy, model_config
import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps
import src.services.team.schema as tms

class CntCollector(ICollector):
    def __init__(self, alias):
        self.alias = alias
        self.counter = 0

    def add(self, val):
        self.counter = self.counter + len(val)

    def values(self):
        return self.counter

@model_config()
class Sample4TeamDetail(tms.Team):
    sprints: Annotated[list[Sample4SprintDetail], LoadBy('id')] = []

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])
    
    total_task_count: int = 0
    def post_total_task_count(self, collector=CntCollector(alias='story_tasks')):
        return collector.values()
    
    description: str = ''
    def post_default_handler(self):
        self.description = f'team: "{self.name}" has {self.task_count} tasks in total.' 

@model_config()
class Sample4SprintDetail(sps.Sprint):
    stories: Annotated[list[Sample4StoryDetail], LoadBy('id')] = []

    task_count: int = 0
    # task_count: int = Field(default=0, exclude=True)
    def post_task_count(self):
        return sum([s.task_count for s in self.stories])

@model_config()
class Sample4StoryDetail(ss.Story):
    __pydantic_resolve_collect__ = {'tasks': 'story_tasks'}

    tasks: Annotated[list[Sample4TaskDetail], LoadBy('id')] = []
    
    task_count: int = 0
    # task_count: int = Field(default=0, exclude=True)
    def post_task_count(self):
        return len(self.tasks)

@model_config()
class Sample4TaskDetail(ts.Task):
    user: Annotated[Optional[us.User], LoadBy('owner_id')] = None
