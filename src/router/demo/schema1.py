from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_resolve import Loader, Collector, ensure_subset
from src.services.story.schema import Story as BaseStory

from src.services.task.schema import Task as BaseTask
from src.services.task.loader import story_to_task_loader

from src.services.user.schema import User as BaseUser
from src.services.user.loader import user_batch_loader


# post case 1
class Task1(BaseTask):
    __pydantic_resolve_collect__ = {'user': 'related_users'}  # Propagate user to collector: 'related_users'
    
    user: Optional[BaseUser] = None
    def resolve_user(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None

@ensure_subset(BaseStory)
class Story1(BaseModel):
    id: int
    name: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

    tasks: list[Task1] = []
    def resolve_tasks(self, loader=Loader(story_to_task_loader)):
        return loader.load(self.id)

    assignee: Optional[BaseUser] = None
    def resolve_assignee(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None

    related_users: list[BaseUser] = []
    def post_related_users(self, collector=Collector(alias='related_users')):
        return collector.values()

