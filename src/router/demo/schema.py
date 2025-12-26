from typing import Optional, Annotated
from pydantic_resolve import LoadBy
from src.services.story.schema import Story as BaseStory
from src.services.task.schema import Task as BaseTask
from src.services.user.schema import User as BaseUser

class Task(BaseTask):
    user: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

class Story(BaseStory):
    tasks: Annotated[list[Task], LoadBy('id')] = []
    assignee: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None
