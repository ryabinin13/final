from datetime import datetime
from app.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Meeting(Base):

    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    discription: Mapped[str]
    date: Mapped[datetime]