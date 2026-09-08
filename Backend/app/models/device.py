from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
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
    hostname: Mapped[str | None] = mapped_column(String(255), index=True)
    ip_address: Mapped[str | None] = mapped_column(String(128), index=True)
    mac_address: Mapped[str | None] = mapped_column(String(64))
    device_type: Mapped[str] = mapped_column(String(50), default="unknown")
    network_interface: Mapped[str | None] = mapped_column(String(100))
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    last_telemetry_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(String(20), default="UNKNOWN", index=True)
    authorization_state: Mapped[str] = mapped_column(String(20), default="PENDING", index=True)
    authorized_by: Mapped[str | None] = mapped_column(String(36))
    authorized_at: Mapped[datetime | None] = mapped_column(DateTime)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    monitoring_scope: Mapped[dict] = mapped_column(JSON, default=dict)
    consent_reference: Mapped[str | None] = mapped_column(String(255))
    data_source: Mapped[str] = mapped_column(String(20), default="REAL")
    trust_score: Mapped[float] = mapped_column(Float, default=50.0)
    user = relationship("User", back_populates="devices")
