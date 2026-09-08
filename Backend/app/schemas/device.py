from datetime import datetime

from pydantic import BaseModel, Field


AUTHORIZATION_STATES = {"PENDING", "AUTHORIZED", "ACTIVE", "REVOKED", "EXPIRED"}


class DeviceRegisterRequest(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip_address: str | None = Field(default=None, max_length=128)
    mac_address: str | None = Field(default=None, max_length=64)
    browser: str = Field(default="SENTINEL Collector", max_length=100)
    operating_system: str = Field(default="unknown", max_length=100)
    device_type: str = Field(default="unknown", max_length=50)
    network_interface: str | None = Field(default=None, max_length=100)
    monitoring_scope: dict = Field(default_factory=dict)
    consent_reference: str | None = Field(default=None, max_length=255)


class DeviceAuthorizationRequest(BaseModel):
    consent_reference: str | None = Field(default=None, max_length=255)
    monitoring_scope: dict = Field(default_factory=dict)
    expires_at: datetime | None = None


class DeviceRead(BaseModel):
    id: str
    hostname: str | None
    ip_address: str | None
    mac_address: str | None
    device_type: str
    operating_system: str
    network_interface: str | None
    first_seen: datetime
    last_seen: datetime
    last_telemetry_at: datetime | None
    status: str
    authorization_state: str
    authorized_by: str | None
    authorized_at: datetime | None
    expires_at: datetime | None
    monitoring_scope: dict
    consent_reference: str | None
    data_source: str
