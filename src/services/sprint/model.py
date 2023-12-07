from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
import src.db as db

class Sprint(db.Base):
    __tablename__ = "sprint"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    status: Mapped[str] = mapped_column(String(100))
    team_id: Mapped[int]