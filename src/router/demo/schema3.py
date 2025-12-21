from typing import Optional, Annotated
from pydantic_resolve import DefineSubset, LoadBy, ExposeAs
from src.services.story.schema import Story as BaseStory

from src.services.task.schema import Task as BaseTask
from src.services.user.schema import User as BaseUser


# post case 1
class Task3(BaseTask):
    user: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None

    fullname: str = ''
    def post_fullname(self, ancestor_context):  # Access story.name from parent context
        return f'{ancestor_context["story_name"]} - {self.name}'

class Story3(DefineSubset):
    __subset__ = (BaseStory, ('id', 'name', 'owner_id'))
    __pydantic_resolve_expose__ = {'name': 'story_name'}

    tasks: Annotated[list[Task3], LoadBy('id')] = []
    assignee: Annotated[Optional[BaseUser], LoadBy('owner_id')] = None