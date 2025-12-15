from pydantic import BaseModel, ConfigDict
from pydantic_resolve import Relationship
import src.services.task.loader as task_loader
import src.services.user.loader as user_loader
import src.services.user.schema as user_schema
import src.services.task.schema as task_schema
from src.services.er_diagram import BaseEntity

class Story(BaseModel, BaseEntity):
    __pydantic_resolve_relationships__ = [
        Relationship( field='id', target_kls=list[task_schema.Task], loader=task_loader.story_to_task_loader),
        Relationship( field='owner_id', target_kls=user_schema.User, loader=user_loader.user_batch_loader)
    ]

    id: int
    name: str
    owner_id: int
    sprint_id: int

    model_config = ConfigDict(from_attributes=True)

