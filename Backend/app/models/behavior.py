from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.helpers import utc_now


class BehaviorSample(Base):
    __tablename__ = "behavior_samples"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    typing_speed: Mapped[float | None] = mapped_column(Float)
    key_press_mean_ms: Mapped[float | None] = mapped_column(Float)
    key_release_mean_ms: Mapped[float | None] = mapped_column(Float)
    mouse_speed: Mapped[float | None] = mapped_column(Float)
    mouse_acceleration: Mapped[float | None] = mapped_column(Float)
    click_frequency: Mapped[float | None] = mapped_column(Float)
    session_duration_seconds: Mapped[int | None] = mapped_column(Integer)
    login_hour: Mapped[int] = mapped_column(Integer)
    device_fingerprint_hash: Mapped[str | None] = mapped_column(String(128))
    region: Mapped[str | None] = mapped_column(String(100))
    network_hash: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class BehavioralBaseline(Base):
    __tablename__ = "behavioral_baselines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    baseline_type: Mapped[str] = mapped_column(String(50), default="default")
    statistical_data: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)
