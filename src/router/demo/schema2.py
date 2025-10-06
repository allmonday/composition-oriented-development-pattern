from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_resolve import Loader, ensure_subset
from src.services.story.schema import Story as BaseStory

from src.services.task.schema import Task as BaseTask
from src.services.task.loader import story_to_task_loader

from src.services.user.schema import User as BaseUser
from src.services.user.loader import user_batch_loader


# post case 1
class Task2(BaseTask):
    user: Optional[BaseUser] = None
    def resolve_user(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None

@ensure_subset(BaseStory)
class Story2(BaseModel):
    id: int
    name: str
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

    tasks: list[Task2] = []
    def resolve_tasks(self, loader=Loader(story_to_task_loader)):
        return loader.load(self.id)

    assignee: Optional[BaseUser] = None
    def resolve_assignee(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None

    total_estimate: int = 0
    def post_total_estimate(self):
        return sum(task.estimate for task in self.tasks)

