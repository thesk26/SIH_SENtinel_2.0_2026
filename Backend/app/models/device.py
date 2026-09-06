from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.helpers import utc_now


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    device_fingerprint_hash: Mapped[str] = mapped_column(String(128), index=True)
    browser: Mapped[str] = mapped_column(String(100))
    operating_system: Mapped[str] = mapped_column(String(100))
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    trust_score: Mapped[float] = mapped_column(Float, default=50.0)
    user = relationship("User", back_populates="devices")
