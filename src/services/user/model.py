from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import src.db as db

class User(db.Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    level: Mapped[str]