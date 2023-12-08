from typing import List, Optional
from pydantic2_resolve import LoaderDepend

import src.services.task.loader as tl
import src.services.user.loader as ul
import src.services.story.loader as sl

import src.services.story.schema as ss
import src.services.task.schema as ts
import src.services.user.schema as us
import src.services.sprint.schema as sps


class Sample1TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)

class Sample1StoryDetail(ss.Story):
    tasks: list[Sample1TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_tasks_loader)):
        return loader.load(self.id)
    
class Sample1SprintDetail(sps.Sprint):
    stories: list[Sample1StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_story_loader)):
        return loader.load(self.id)