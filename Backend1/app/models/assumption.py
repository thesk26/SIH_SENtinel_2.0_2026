from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Assumption(Base):
    __tablename__ = "assumptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    assumption_type: Mapped[str] = mapped_column(String(50), index=True)
    value_hash_or_reference: Mapped[str] = mapped_column(String(255))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    frequency: Mapped[float] = mapped_column(Float, default=0.0)
    last_observed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    risk_weight: Mapped[float] = mapped_column(Float, default=1.0)
    status: Mapped[str] = mapped_column(String(20), default="CANDIDATE", index=True)
    supporting_events: Mapped[int] = mapped_column(Integer, default=0)
    contradicting_events: Mapped[int] = mapped_column(Integer, default=0)
    first_verified: Mapped[datetime | None] = mapped_column(DateTime)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
