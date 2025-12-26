from typing import Optional, Annotated
from pydantic_resolve import Collector, DefineSubset, LoadBy, SendTo
from src.services.story.schema import Story as BaseStory
from src.services.task.schema import Task as BaseTask
from src.services.user.schema import User as BaseUser


# post case 1
class Task1(BaseTask):
    user: Annotated[
        Optional[BaseUser], 
        LoadBy('owner_id'), 
        SendTo('related_users')] = None

class Story1(DefineSubset):
    __subset__ = (BaseStory, ('id', 'name', 'owner_id'))

    tasks: Annotated[list[Task1], LoadBy('id')] = []
    assignee: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

    related_users: list[BaseUser] = []
    def post_related_users(self, collector=Collector(alias='related_users')):
        return collector.values()

