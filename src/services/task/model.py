from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import src.db as db

class Task(db.Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int]
    story_id: Mapped[int]
    estimate: Mapped[int]