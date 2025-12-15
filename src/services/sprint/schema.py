from pydantic import BaseModel, ConfigDict
from pydantic_resolve import Relationship
import src.services.story.schema as story_schema
import src.services.story.loader as story_loader
from src.services.er_diagram import BaseEntity

class Sprint(BaseModel, BaseEntity):
    __pydantic_resolve_relationships__ = [
        Relationship( field='id', target_kls=list[story_schema.Story], loader=story_loader.sprint_to_story_loader)
    ]

    id: int
    name: str
    status: str
    team_id: int

    model_config = ConfigDict(from_attributes=True)
