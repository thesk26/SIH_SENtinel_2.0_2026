from datetime import datetime

from pydantic import BaseModel, Field


class BehaviorCollect(BaseModel):
    typing_speed: float | None = Field(default=None, ge=0, le=500)
    key_press_mean_ms: float | None = Field(default=None, ge=0, le=10000)
    key_release_mean_ms: float | None = Field(default=None, ge=0, le=10000)
    mouse_speed: float | None = Field(default=None, ge=0, le=100000)
    mouse_acceleration: float | None = Field(default=None, ge=0, le=100000)
    click_frequency: float | None = Field(default=None, ge=0, le=1000)
    session_duration_seconds: int | None = Field(default=None, ge=0, le=86400)
    login_hour: int = Field(ge=0, le=23)
    device_fingerprint: str | None = Field(default=None, min_length=1, max_length=512)
    region: str | None = Field(default=None, max_length=100)
    network_identifier: str | None = Field(default=None, min_length=1, max_length=512)


class BaselineRead(BaseModel):
    user_id: str
    baseline_type: str
    statistical_data: dict
    confidence: float
    updated_at: datetime
