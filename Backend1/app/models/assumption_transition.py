from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.helpers import utc_now


class AssumptionTransition(Base):
    __tablename__ = "assumption_transitions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    assumption_id: Mapped[str] = mapped_column(ForeignKey("assumptions.id"), index=True)
    previous_status: Mapped[str] = mapped_column(String(20))
    new_status: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
