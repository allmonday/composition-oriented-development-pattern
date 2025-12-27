from typing import Optional
from pydantic_resolve import Loader, model_config, SubsetConfig, DefineSubset
from typing import Dict

import src.services.task.loader as tl
import src.services.user.loader as ul
import src.services.story.loader as sl
import src.services.sprint.loader as spl

import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps
import src.services.team.schema as tms

class Sample3TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=Loader(ul.user_batch_loader)):
        return loader.load(self.owner_id)
    
    full_name: str = ''
    def resolve_full_name(self, ancestor_context: Dict):
        team = ancestor_context['team_name']
        sprint = ancestor_context['sprint_name']
        story = ancestor_context['story_name']
        return f"{team}/{sprint}/{story}/{self.name}"

class Sample3StoryDetail(DefineSubset):
    __subset__ = SubsetConfig(
        kls=ss.Story,
        fields="all",
        expose_as=[('name', 'story_name')]
    )
    tasks: list[Sample3TaskDetail] = []
    def resolve_tasks(self, loader=Loader(tl.story_to_task_loader)):
        return loader.load(self.id)
    
class Sample3SprintDetail(DefineSubset):
    __subset__ = SubsetConfig(
        kls=sps.Sprint,
        fields="all",
        expose_as=[('name', 'sprint_name')]
    )

    stories: list[Sample3StoryDetail] = []
    def resolve_stories(self, loader=Loader(sl.sprint_to_story_loader)):
        return loader.load(self.id)

class Sample3TeamDetail(DefineSubset):
    __subset__ = SubsetConfig(
        kls=tms.Team,
        fields="all",
        expose_as=[('name', 'team_name')]
    )

    sprints: list[Sample3SprintDetail] = []
    def resolve_sprints(self, loader=Loader(spl.team_to_sprint_loader)):
        return loader.load(self.id)