from typing import Optional
from pydantic_resolve import Loader, Collector
from src.services.story.schema import Story as BaseStory

from src.services.task.schema import Task as BaseTask
from src.services.task.loader import story_to_task_loader

from src.services.user.schema import User as BaseUser
from src.services.user.loader import user_batch_loader


class Task(BaseTask):
    user: Optional[BaseUser] = None
    def resolve_user(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None

class Story(BaseStory):
    tasks: list[Task] = []
    def resolve_tasks(self, loader=Loader(story_to_task_loader)):
        return loader.load(self.id)

    assignee: Optional[BaseUser] = None
    def resolve_assignee(self, loader=Loader(user_batch_loader)):
        return loader.load(self.owner_id) if self.owner_id else None
