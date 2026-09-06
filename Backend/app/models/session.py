from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.helpers import utc_now


class SessionRecord(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    session_identifier: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
