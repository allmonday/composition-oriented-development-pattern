from pydantic import BaseModel, ConfigDict

class Sprint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    team_id: int

