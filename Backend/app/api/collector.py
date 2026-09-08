from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException
from sqlalchemy import desc, func, select

from app.core.config import settings
from app.core.dependencies import CurrentUser, DbSession
from app.models.device import Device
from app.models.network_traffic import NetworkTraffic
from app.models.security_event import SecurityEvent
from app.models.telemetry import TelemetrySample
from app.schemas.telemetry import HeartbeatRequest, TelemetryRead, TelemetryRequest
from app.utils.helpers import utc_now

router = APIRouter(prefix="/collector", tags=["collector"])
public_router = APIRouter(tags=["collector"])


def active_device(device_id: str, current_user: CurrentUser, db: DbSession) -> Device:
    device = db.scalar(select(Device).where(Device.id == device_id, Device.user_id == current_user.id))
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    if device.authorization_state != "ACTIVE":
        raise HTTPException(status_code=403, detail=f"Device monitoring is {device.authorization_state}; collection is denied")
    if device.expires_at and device.expires_at <= datetime.now(UTC).replace(tzinfo=None):
        device.authorization_state = "EXPIRED"
        device.status = "UNKNOWN"
        db.commit()
        raise HTTPException(status_code=403, detail="Device authorization has expired")
    return device


def observed_at(timestamp: datetime | None) -> datetime:
    return (timestamp or datetime.now(UTC)).astimezone(UTC).replace(tzinfo=None)


@router.post("/heartbeat")
def heartbeat(payload: HeartbeatRequest, current_user: CurrentUser, db: DbSession):
    device = active_device(payload.device_id, current_user, db)
    timestamp = observed_at(payload.timestamp)
    device.last_telemetry_at = timestamp
    device.last_seen = timestamp
    device.status = "ONLINE"
    db.commit()
    return {"device_id": device.id, "status": device.status, "authorization_state": device.authorization_state, "timestamp": timestamp, "data_source": "REAL"}


@router.post("/telemetry", response_model=TelemetryRead)
def telemetry(payload: TelemetryRequest, current_user: CurrentUser, db: DbSession):
    device = active_device(payload.device_id, current_user, db)
    timestamp = observed_at(payload.timestamp)
    sample = TelemetrySample(user_id=current_user.id, device_id=device.id, timestamp=timestamp, received_at=utc_now(), cpu_percent=payload.cpu_percent, memory_percent=payload.memory_percent, disk_percent=payload.disk_percent, uptime_seconds=payload.uptime_seconds, os_information=payload.os_information, interfaces=payload.interfaces, bytes_sent=payload.bytes_sent, bytes_received=payload.bytes_received, connection_count=payload.connection_count, data_source="REAL")
    device.last_telemetry_at = timestamp
    device.last_seen = timestamp
    device.status = "ONLINE"
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample

@public_router.post("/telemetry", response_model=TelemetryRead)
def telemetry_alias(payload: TelemetryRequest, current_user: CurrentUser, db: DbSession):
    return telemetry(payload, current_user, db)


@router.get("/status")
def collector_status(current_user: CurrentUser, db: DbSession):
    now = utc_now()
    stale_after = timedelta(seconds=settings.collector_stale_seconds)
    devices = db.scalars(select(Device).where(Device.user_id == current_user.id)).all()
    result = []
    for device in devices:
        age = now - device.last_telemetry_at if device.last_telemetry_at else None
        if device.authorization_state != "ACTIVE":
            state = "DISABLED"
        elif age is None:
            state = "OFFLINE"
        elif age > stale_after * 2:
            state = "OFFLINE"
        elif age > stale_after:
            state = "STALE"
        else:
            state = "ONLINE"
        result.append({"device_id": device.id, "hostname": device.hostname, "status": state, "authorization_state": device.authorization_state, "last_heartbeat": device.last_telemetry_at, "data_source": device.data_source})
    return {"collector": "CONNECTED" if any(item["status"] == "ONLINE" for item in result) else "DISCONNECTED", "devices": result, "stale_after_seconds": settings.collector_stale_seconds, "data_source": "REAL"}


@router.get("/diagnostics")
def diagnostics(current_user: CurrentUser, db: DbSession):
    health = {"backend": "HEALTHY", "database": "CONNECTED", "ai": "AVAILABLE" if settings.ml_model_path else "UNAVAILABLE", "blockchain": "UNAVAILABLE"}
    last_telemetry = db.scalar(select(TelemetrySample).where(TelemetrySample.user_id == current_user.id).order_by(desc(TelemetrySample.received_at)))
    return {**health, "collector": collector_status(current_user, db), "last_telemetry": last_telemetry.timestamp if last_telemetry else None, "telemetry_received": db.scalar(select(func.count(TelemetrySample.id)).where(TelemetrySample.user_id == current_user.id)) or 0, "events_processed": db.scalar(select(func.count(SecurityEvent.id)).where(SecurityEvent.user_id == current_user.id)) or 0, "network_events": db.scalar(select(func.count(NetworkTraffic.id)).where(NetworkTraffic.user_id == current_user.id)) or 0, "data_source": "REAL"}
