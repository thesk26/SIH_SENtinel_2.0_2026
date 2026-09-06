from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.helpers import utc_now


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    integrity_score: Mapped[float] = mapped_column(Float)
    decision: Mapped[str] = mapped_column(String(20), index=True)
    signal_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    detected_conflicts: Mapped[list] = mapped_column(JSON, default=list)
    explanation: Mapped[dict] = mapped_column(JSON, default=dict)
    user = relationship("User", back_populates="events")
