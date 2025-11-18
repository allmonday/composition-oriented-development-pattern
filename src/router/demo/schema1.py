from typing import Optional, Annotated
from pydantic_resolve import Collector, DefineSubset, LoadBy
from src.services.story.schema import Story as BaseStory

from src.services.task.schema import Task as BaseTask

from src.services.user.schema import User as BaseUser


# post case 1
class Task1(BaseTask):
    __pydantic_resolve_collect__ = {'user': 'related_users'}  # Propagate user to collector: 'related_users'

    user: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

class Story1(DefineSubset):
    __pydantic_resolve_subset__ = (BaseStory, ('id', 'name', 'owner_id'))

    tasks: Annotated[list[Task1], LoadBy('id')] = []
    assignee: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

    related_users: list[BaseUser] = []
    def post_related_users(self, collector=Collector(alias='related_users')):
        return collector.values()

