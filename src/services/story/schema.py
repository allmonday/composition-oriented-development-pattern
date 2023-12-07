from pydantic import BaseModel

class Story(BaseModel):
    id: int
    name: str
    owner_id: int
    sprint_id: int

