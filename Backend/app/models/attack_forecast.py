from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.helpers import utc_now


class AttackForecast(Base):
    __tablename__ = "attack_forecasts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    event_ids: Mapped[list] = mapped_column(JSON, default=list)
    forecast_available: Mapped[bool] = mapped_column(default=True)
    forecast_source: Mapped[str] = mapped_column(String(30), default="RULE_BASED_FALLBACK")
    predicted_attack_type: Mapped[str] = mapped_column(String(80))
    attack_probability: Mapped[float | None] = mapped_column(Float)
    confidence: Mapped[float | None] = mapped_column(Float)
    potential_targets: Mapped[list] = mapped_column(JSON, default=list)
    risk_level: Mapped[str] = mapped_column(String(20))
    reasoning: Mapped[list] = mapped_column(JSON, default=list)
    ml_probabilities: Mapped[dict] = mapped_column(JSON, default=dict)
    sequence_analysis: Mapped[dict] = mapped_column(JSON, default=dict)
    hybrid_weights: Mapped[dict] = mapped_column(JSON, default=dict)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)
    ml_confidence_level: Mapped[str] = mapped_column(String(10), default="LOW")
    attack_path: Mapped[dict] = mapped_column(JSON, default=dict)
    attack_stage_probabilities: Mapped[dict] = mapped_column(JSON, default=dict)
    attack_stage_evidence: Mapped[dict] = mapped_column(JSON, default=dict)
    contributing_signals: Mapped[list] = mapped_column(JSON, default=list)
    multi_window_analysis: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
