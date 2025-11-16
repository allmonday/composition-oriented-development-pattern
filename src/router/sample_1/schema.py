from __future__ import annotations

from typing import Optional, Annotated
from pydantic_resolve import Loader, model_config, LoadBy

import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps
import src.services.team.schema as tms


@model_config()
class Sample1TeamDetail(tms.Team):
    sprints: Annotated[list[Sample1SprintDetail], LoadBy('id')] = []
    members: Annotated[list[us.User], LoadBy('id')] = []

@model_config()
class Sample1TeamDetail2(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    members: Annotated[list[us.User], LoadBy('id')] = []

@model_config()
class Sample1TaskDetail(ts.Task):
    user: Annotated[Optional[us.User], LoadBy('owner_id')] = None

@model_config()
class Sample1SprintDetail(sps.Sprint):
    stories: Annotated[list[Sample1StoryDetail], LoadBy('id')]  = []

@model_config()
class Sample1StoryDetail(ss.Story):
    tasks: Annotated[list[Sample1TaskDetail], LoadBy('id')] = []
    owner: Annotated[Optional[us.User], LoadBy('owner_id')] = None