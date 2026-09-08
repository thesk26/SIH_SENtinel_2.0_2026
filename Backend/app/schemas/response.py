from datetime import datetime

from pydantic import BaseModel, Field


class ResponseActionRequest(BaseModel):
    action: str = Field(min_length=1, max_length=50)
    device_id: str | None = Field(default=None, max_length=36)
    incident_id: str | None = Field(default=None, max_length=100)
    reason: str = Field(min_length=1, max_length=500)


class ResponseActionRead(BaseModel):
    id: str
    action: str
    device_id: str | None
    status: str
    mode: str
    timestamp: datetime
    audit_id: str


class EvidenceRequest(BaseModel):
    event_id: str | None = Field(default=None, max_length=36)
    device_id: str | None = Field(default=None, max_length=36)
    evidence: dict


class EvidenceRead(BaseModel):
    id: str
    event_id: str | None
    device_id: str | None
    evidence_hash: str
    timestamp: datetime
    data_source: str