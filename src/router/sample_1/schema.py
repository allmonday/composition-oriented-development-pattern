from __future__ import annotations

from typing import Optional
from pydantic_resolve import Loader, model_config

import src.services.task.loader as tl
import src.services.user.loader as ul
import src.services.story.loader as sl
import src.services.sprint.loader as spl

import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps
import src.services.team.schema as tms


@model_config()
class Sample1TeamDetail(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    def resolve_sprints(self, loader=Loader(spl.team_to_sprint_loader)):
        return loader.load(self.id)
    
    members: list[us.User] = []
    def resolve_members(self, loader=Loader(ul.team_to_user_loader)):
        return loader.load(self.id)

@model_config()
class Sample1TeamDetail2(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    
    members: list[us.User] = []
    def resolve_members(self, loader=Loader(ul.team_to_user_loader)):
        return loader.load(self.id)

@model_config()
class Sample1TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=Loader(ul.user_batch_loader)):
        return loader.load(self.owner_id)

@model_config()
class Sample1SprintDetail(sps.Sprint):
    stories: list[Sample1StoryDetail] = []
    def resolve_stories(self, loader=Loader(sl.sprint_to_story_loader)):
        return loader.load(self.id)

@model_config()
class Sample1StoryDetail(ss.Story):
    tasks: list[Sample1TaskDetail] = []
    def resolve_tasks(self, loader=Loader(tl.story_to_task_loader)):
        return loader.load(self.id)

    owner: Optional[us.User] = None
    def resolve_owner(self, loader=Loader(ul.user_batch_loader)):
        return loader.load(self.owner_id)