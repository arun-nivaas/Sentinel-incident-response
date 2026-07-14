from datetime import datetime
from sqlalchemy import Text,String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base


class RawIncident(Base):

    __tablename__ = "raw_incidents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    received_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    source: Mapped[str] = mapped_column(String, default="webhook")
    raw_payload: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")


