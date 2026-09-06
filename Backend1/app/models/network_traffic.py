from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.helpers import utc_now


class NetworkTraffic(Base):
    __tablename__ = "network_traffic"
    __table_args__ = (
        Index("ix_network_traffic_user_timestamp", "user_id", "timestamp"),
        Index("ix_network_traffic_relationship", "user_id", "source_entity", "destination_entity"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    source_entity: Mapped[str] = mapped_column(String(128), index=True)
    destination_entity: Mapped[str] = mapped_column(String(128), index=True)
    source_port: Mapped[int | None] = mapped_column(Integer)
    destination_port: Mapped[int | None] = mapped_column(Integer)
    protocol: Mapped[str] = mapped_column(String(20))
    packet_count: Mapped[int] = mapped_column(Integer)
    byte_count: Mapped[int] = mapped_column(Integer)
    flow_duration_ms: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    tcp_flags: Mapped[str | None] = mapped_column(String(32))
    connection_status: Mapped[str] = mapped_column(String(30))
    request_frequency: Mapped[float] = mapped_column(Float)
    baseline_eligible: Mapped[bool] = mapped_column(default=True, index=True)
    source_event_id: Mapped[str | None] = mapped_column(String(128), index=True)
    event_fingerprint: Mapped[str | None] = mapped_column(String(64), index=True)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    ingestion_source: Mapped[str] = mapped_column(String(30), default="REST")
    derived_features: Mapped[dict] = mapped_column(JSON, default=dict)
