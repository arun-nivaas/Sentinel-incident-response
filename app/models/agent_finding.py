from datetime import datetime
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base
from typing import Optional,Any,Dict
from sqlalchemy.dialects.postgresql import JSONB


class AgentFinding(Base):
  
    __tablename__ = "agent_findings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    raw_incident_id: Mapped[int] = mapped_column(ForeignKey("raw_incidents.id"), nullable=False)
    agent_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    output: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())