from typing import Optional, Annotated
from pydantic_resolve import LoadBy
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
    stories: Annotated[list[ss.Story], LoadBy('id')] = []

class Sample7TeamDetail(tms.Team):
    sprints: Annotated[list[Sample7SprintDetail], LoadBy('id')] = []

class Sample7TaskDetail(ts.Task):
    user: Annotated[Optional[us.User], LoadBy('owner_id')] = None