from datetime import datetime
from sqlalchemy import Text,String,Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base

class ParsedIncident(Base):

    __tablename__ = "parsed_incidents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    raw_incident_id: Mapped[int] = mapped_column(nullable=False)
    service_name: Mapped[str | None] = mapped_column(String, nullable=True)
    endpoint: Mapped[str | None] = mapped_column(String, nullable=True)
    error_type: Mapped[str | None] = mapped_column(String, nullable=True)
    stack_trace: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurrence_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    occurred_at: Mapped[datetime | None] = mapped_column(nullable=True)
    parsed_at: Mapped[datetime] = mapped_column(server_default=func.now())
    severity_hint: Mapped[str | None] = mapped_column(String, nullable=True)
    fingerprint: Mapped[str] = mapped_column(String, nullable=False, index=True)