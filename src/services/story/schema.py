from pydantic import BaseModel, ConfigDict

class Story(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    owner_id: int
    sprint_id: int

