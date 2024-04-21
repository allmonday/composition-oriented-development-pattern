from __future__ import annotations

from typing import List, Optional
from pydantic import Field
from pydantic_resolve import LoaderDepend, model_config, ICollector

import src.services.task.loader as tl
import src.services.user.loader as ul
import src.services.story.loader as sl
import src.services.sprint.loader as spl

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

class Sample4TeamDetail(tms.Team):
    sprints: list[Sample4SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])
    
    total_task_count: int = 0
    def post_total_task_count(self, collector=CntCollector(alias='story_tasks')):
        return collector.values()
    
    description: str = ''
    def post_default_handler(self):
        self.description = f'team: "{self.name}" has {self.task_count} tasks in total.' 

# @model_config()
class Sample4SprintDetail(sps.Sprint):
    stories: list[Sample4StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

    task_count: int = 0
    # task_count: int = Field(default=0, exclude=True)
    def post_task_count(self):
        return sum([s.task_count for s in self.stories])

# @model_config()
class Sample4StoryDetail(ss.Story):
    __pydantic_resolve_collect__ = {'tasks': 'story_tasks'}

    tasks: list[Sample4TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)
    
    task_count: int = 0
    # task_count: int = Field(default=0, exclude=True)
    def post_task_count(self):
        return len(self.tasks)

class Sample4TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
