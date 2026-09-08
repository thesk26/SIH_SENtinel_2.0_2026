from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field, field_validator


class NetworkTrafficCreate(BaseModel):
    device_id: str | None = Field(default=None, max_length=36)
    source_event_id: str | None = Field(default=None, max_length=128)
    ingestion_source: str = Field(default="REST", min_length=1, max_length=30)
    source_ip: str = Field(min_length=1, max_length=128)
    destination_ip: str = Field(min_length=1, max_length=128)
    source_port: int | None = Field(default=None, ge=0, le=65535)
    destination_port: int | None = Field(default=None, ge=0, le=65535)
    protocol: str = Field(default="TCP", min_length=1, max_length=20)
    packet_count: int = Field(ge=0, le=10_000_000)
    byte_count: int = Field(ge=0, le=10_000_000_000)
    flow_duration_ms: int = Field(default=0, ge=0, le=86_400_000)
    timestamp: datetime | None = None
    tcp_flags: str | None = Field(default=None, max_length=32)
    connection_status: str = Field(default="success", min_length=1, max_length=30)
    request_frequency: float = Field(default=1.0, ge=0, le=1_000_000)

    @field_validator("timestamp")
    @classmethod
    def reject_far_future_timestamp(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        current = datetime.now(timezone.utc)
        comparable = value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value
        if comparable > current + timedelta(minutes=5):
            raise ValueError("timestamp cannot be more than five minutes in the future")
        return value


class NetworkTrafficRead(BaseModel):
    id: str
    device_id: str | None = None
    timestamp: datetime
    source_entity: str
    destination_entity: str
    protocol: str
    destination_port: int | None
    derived_features: dict
    baseline_eligible: bool
    event_fingerprint: str | None = None
    is_duplicate: bool = False


class NetworkBaselineRead(BaseModel):
    entity_id: str
    baseline: dict


class NetworkAnalysisResponse(BaseModel):
    flow_id: str
    features: dict
    integrity_score: float
    signal_scores: dict[str, float]
    relationship_score: float
    conflicts: list[str]
    decision: str
    baseline_eligible: bool
    forecast: dict


class ForecastRead(BaseModel):
    id: str
    forecast_available: bool
    forecast_source: str
    ml_model_loaded: bool
    predicted_attack_type: str
    attack_probability: float | None
    confidence: float | None
    potential_targets: list[dict]
    risk_level: str
    reasoning: list[str]
    ml_probabilities: dict[str, float] = Field(default_factory=dict)
    sequence_analysis: dict = Field(default_factory=dict)
    attack_path: dict = Field(default_factory=dict)
    attack_stage_probabilities: dict[str, float] = Field(default_factory=dict)
    attack_stage_evidence: dict = Field(default_factory=dict)
    contributing_signals: list[dict] = Field(default_factory=list)
    multi_window_analysis: dict = Field(default_factory=dict)
    hybrid_weights: dict[str, float] = Field(default_factory=dict)
    evidence: dict = Field(default_factory=dict)
    ml_confidence_level: str = "LOW"
    relationship_analysis_available: bool = False
    integrity_analysis_available: bool = False
    created_at: datetime
