from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HeartbeatRequest(BaseModel):
    device_id: str = Field(min_length=1, max_length=36)
    timestamp: datetime | None = None
    status: str = Field(default="online", min_length=1, max_length=20)


class TelemetryRequest(BaseModel):
    device_id: str = Field(min_length=1, max_length=36)
    timestamp: datetime | None = None
    cpu_percent: float | None = Field(default=None, ge=0, le=100)
    memory_percent: float | None = Field(default=None, ge=0, le=100)
    disk_percent: float | None = Field(default=None, ge=0, le=100)
    uptime_seconds: int | None = Field(default=None, ge=0)
    os_information: dict = Field(default_factory=dict)
    interfaces: dict = Field(default_factory=dict)
    bytes_sent: int | None = Field(default=None, ge=0)
    bytes_received: int | None = Field(default=None, ge=0)
    connection_count: int | None = Field(default=None, ge=0)


class TelemetryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    device_id: str
    timestamp: datetime
    received_at: datetime
    data_source: str
