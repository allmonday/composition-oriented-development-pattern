from pydantic import BaseModel, ConfigDict
from src.services.er_diagram import BaseEntity
from pydantic_resolve import Relationship
import src.services.user.loader as user_loader
import src.services.user.schema as user_schema

class Task(BaseModel, BaseEntity):
    __pydantic_resolve_relationships__ = [
        Relationship( field='owner_id', target_kls=user_schema.User, loader=user_loader.user_batch_loader)
    ]
    id: int
    name: str
    owner_id: int
    story_id: int
    estimate: int

    model_config = ConfigDict(from_attributes=True)