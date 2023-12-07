from pydantic import BaseModel

class Sprint(BaseModel):
    id: int
    name: str
    status: str
    team_id: str

