from pydantic import BaseModel, ConfigDict

class Task(BaseModel):
    id: int
    name: str
    owner_id: int
    story_id: int
    estimate: int

    model_config = ConfigDict(from_attributes=True)