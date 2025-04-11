from typing import Optional
from sqlalchemy import Date, Integer, Sequence, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date
import uuid


class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int]
    user_id: Mapped[uuid.UUID]
    mark: Mapped[int]
    comment: Mapped[str] = mapped_column(nullable=True)