from typing import Optional, Annotated
from pydantic_resolve import DefineSubset, LoadBy
from src.services.story.schema import Story as BaseStory
from src.services.task.schema import Task as BaseTask
from src.services.user.schema import User as BaseUser


# post case 1
class Task2(BaseTask):
    user: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

class Story2(DefineSubset):
    __pydantic_resolve_subset__ = (BaseStory, ('id', 'name', 'owner_id'))

    tasks: Annotated[list[Task2], LoadBy('id')] = []
    assignee: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

    total_estimate: int = 0
    def post_total_estimate(self):
        return sum(task.estimate for task in self.tasks)

