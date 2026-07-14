from datetime import datetime
from sqlalchemy import String,Integer,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base
from typing import Optional


class GithubActionFinding(Base):

    __tablename__ = "github_action_findings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    raw_incident_id: Mapped[int] = mapped_column(ForeignKey("raw_incidents.id"), nullable=False)
    issue_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    issue_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())