from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import src.db as db

class Story(db.Base):
    __tablename__ = "story"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int]
    sprint_id: Mapped[int]