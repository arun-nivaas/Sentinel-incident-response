from datetime import datetime
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database.database import Base


class Postmortem(Base):
    __tablename__ = "postmortems"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_name: Mapped[str] = mapped_column(String, nullable=False)
    error_type: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())