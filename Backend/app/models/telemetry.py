from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.helpers import utc_now


class TelemetrySample(Base):
    __tablename__ = "telemetry_samples"
    __table_args__ = (Index("ix_telemetry_device_timestamp", "device_id", "timestamp"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    device_id: Mapped[str] = mapped_column(ForeignKey("devices.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    cpu_percent: Mapped[float | None] = mapped_column(Float)
    memory_percent: Mapped[float | None] = mapped_column(Float)
    disk_percent: Mapped[float | None] = mapped_column(Float)
    uptime_seconds: Mapped[int | None] = mapped_column(Integer)
    os_information: Mapped[dict] = mapped_column(JSON, default=dict)
    interfaces: Mapped[dict] = mapped_column(JSON, default=dict)
    bytes_sent: Mapped[int | None] = mapped_column(Integer)
    bytes_received: Mapped[int | None] = mapped_column(Integer)
    packets_sent: Mapped[int | None] = mapped_column(Integer)
    packets_received: Mapped[int | None] = mapped_column(Integer)
    connection_count: Mapped[int | None] = mapped_column(Integer)
    process_count: Mapped[int | None] = mapped_column(Integer)
    service_count: Mapped[int | None] = mapped_column(Integer)
    memory_total_bytes: Mapped[int | None] = mapped_column(Integer)
    memory_available_bytes: Mapped[int | None] = mapped_column(Integer)
    memory_used_bytes: Mapped[int | None] = mapped_column(Integer)
    disk_total_bytes: Mapped[int | None] = mapped_column(Integer)
    disk_free_bytes: Mapped[int | None] = mapped_column(Integer)
    data_source: Mapped[str] = mapped_column(String(20), default="REAL")