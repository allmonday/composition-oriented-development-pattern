from pydantic import BaseModel, ConfigDict
from pydantic_resolve import Relationship
import src.services.sprint.schema as sprint_schema
import src.services.sprint.loader as sprint_loader
import src.services.user.schema as user_schema
import src.services.user.loader as user_loader
from src.services.er_diagram import BaseEntity

class Team(BaseModel, BaseEntity):
    __pydantic_resolve_relationships__ = [
        Relationship( field='id', target_kls=list[sprint_schema.Sprint], loader=sprint_loader.team_to_sprint_loader),
        Relationship( field='id', target_kls=list[user_schema.User], loader=user_loader.team_to_user_loader)
    ]
    
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
