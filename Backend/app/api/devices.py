from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.dependencies import CurrentUser, DbSession
from app.core.config import settings
from app.models.device import Device
from app.schemas.device import DeviceAuthorizationRequest, DeviceRead, DeviceRegisterRequest
from app.utils.helpers import hash_identifier, utc_now

router = APIRouter(prefix="/devices", tags=["devices"])


def _read(device: Device) -> DeviceRead:
    now = utc_now()
    if device.authorization_state != "ACTIVE":
        current_status = "UNKNOWN"
    elif not device.last_telemetry_at:
        current_status = "OFFLINE"
    else:
        age = now - device.last_telemetry_at
        current_status = "OFFLINE" if age.total_seconds() > settings.collector_stale_seconds * 2 else "STALE" if age.total_seconds() > settings.collector_stale_seconds else "ONLINE"
    return DeviceRead(
        id=device.id,
        hostname=device.hostname,
        ip_address=device.ip_address,
        mac_address=device.mac_address,
        device_type=device.device_type,
        operating_system=device.operating_system,
        network_interface=device.network_interface,
        first_seen=device.first_seen,
        last_seen=device.last_seen,
        last_telemetry_at=device.last_telemetry_at,
        status=current_status,
        authorization_state=device.authorization_state,
        authorized_by=device.authorized_by,
        authorized_at=device.authorized_at,
        expires_at=device.expires_at,
        monitoring_scope=device.monitoring_scope or {},
        consent_reference=device.consent_reference,
        data_source=device.data_source,
    )


def _owned(device_id: str, current_user: CurrentUser, db: DbSession) -> Device:
    device = db.scalar(select(Device).where(Device.id == device_id, Device.user_id == current_user.id))
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def register_device(payload: DeviceRegisterRequest, current_user: CurrentUser, db: DbSession):
    device = Device(
        user_id=current_user.id,
        device_fingerprint_hash=hash_identifier(payload.mac_address or payload.hostname) or "unknown",
        browser=payload.browser,
        operating_system=payload.operating_system,
        hostname=payload.hostname,
        ip_address=payload.ip_address,
        mac_address=payload.mac_address,
        device_type=payload.device_type,
        network_interface=payload.network_interface,
        monitoring_scope=payload.monitoring_scope,
        consent_reference=payload.consent_reference,
        data_source="REAL",
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return _read(device)


@router.get("", response_model=list[DeviceRead])
def list_devices(current_user: CurrentUser, db: DbSession):
    return [_read(device) for device in db.scalars(select(Device).where(Device.user_id == current_user.id).order_by(Device.last_seen.desc())).all()]


@router.post("/{device_id}/authorize", response_model=DeviceRead)
def authorize_device(device_id: str, payload: DeviceAuthorizationRequest, current_user: CurrentUser, db: DbSession):
    device = _owned(device_id, current_user, db)
    device.authorization_state = "AUTHORIZED"
    device.authorized_by = current_user.id
    device.authorized_at = utc_now()
    device.expires_at = payload.expires_at.replace(tzinfo=None) if payload.expires_at else None
    device.monitoring_scope = payload.monitoring_scope
    device.consent_reference = payload.consent_reference or device.consent_reference
    db.commit()
    db.refresh(device)
    return _read(device)


@router.post("/{device_id}/activate", response_model=DeviceRead)
def activate_device(device_id: str, current_user: CurrentUser, db: DbSession):
    device = _owned(device_id, current_user, db)
    if device.authorization_state != "AUTHORIZED":
        raise HTTPException(status_code=409, detail="Device must be AUTHORIZED before activation")
    if device.expires_at and device.expires_at <= datetime.now(UTC).replace(tzinfo=None):
        device.authorization_state = "EXPIRED"
        db.commit()
        raise HTTPException(status_code=409, detail="Device authorization has expired")
    device.authorization_state = "ACTIVE"
    device.status = "UNKNOWN"
    db.commit()
    db.refresh(device)
    return _read(device)


@router.post("/{device_id}/revoke", response_model=DeviceRead)
def revoke_device(device_id: str, current_user: CurrentUser, db: DbSession):
    device = _owned(device_id, current_user, db)
    device.authorization_state = "REVOKED"
    device.status = "UNKNOWN"
    db.commit()
    db.refresh(device)
    return _read(device)
