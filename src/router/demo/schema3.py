from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_resolve import Loader, ensure_subset
from src.services.story.schema import Story as BaseStory

from src.services.task.schema import Task as BaseTask
from src.services.task.loader import story_to_task_loader

from src.services.user.schema import User as BaseUser
from src.services.user.loader import user_batch_loader


# post case 1
class Task3(BaseTask):
    user: Optional[BaseUser] = None
    def resolve_user(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None

    fullname: str = ''
    def post_fullname(self, ancestor_context):  # Access story.name from parent context
        return f'{ancestor_context["story_name"]} - {self.name}'

@ensure_subset(BaseStory)
class Story3(BaseModel):
    __pydantic_resolve_expose__ = {'name': 'story_name'}

    id: int
    name: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

    tasks: list[Task3] = []
    def resolve_tasks(self, loader=Loader(story_to_task_loader)):
        return loader.load(self.id)

    assignee: Optional[BaseUser] = None
    def resolve_assignee(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None