from typing import List, Optional
from pydantic_resolve import LoaderDepend
from pydantic_resolve.util import generate_list_empty_loader, generate_single_empty_loader
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


SprintToStoryLoader = generate_list_empty_loader('SprintToStoryLoader')
TeamToSprintLoader = generate_list_empty_loader('TeamToSprintLoader')
UserLoader = generate_single_empty_loader('UserLoader')

class Sample7SprintDetail(sps.Sprint):
    stories: list[ss.Story] = []
    def resolve_stories(self, loader=LoaderDepend(SprintToStoryLoader)):
        return loader.load(self.id)

class Sample7TeamDetail(tms.Team):
    sprints: list[Sample7SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(TeamToSprintLoader)):
        return loader.load(self.id)

class Sample7TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(UserLoader)):
        return loader.load(self.owner_id)