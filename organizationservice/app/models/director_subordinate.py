import uuid
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class DirectorSubordinate(Base):
    __tablename__ = "director_subordinate"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    director_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    subordinate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))