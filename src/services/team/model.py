from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import src.db as db

class Team(db.Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

class TeamUser(db.Base):
    __tablename__ = "team_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    team_id: Mapped[int]