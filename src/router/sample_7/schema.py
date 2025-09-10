from typing import Optional
from pydantic_resolve import LoaderDepend
from pydantic_resolve.utils.dataloader import generate_list_empty_loader, generate_single_empty_loader


import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps
import src.services.team.schema as tms



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