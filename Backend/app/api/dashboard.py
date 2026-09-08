from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter
from sqlalchemy import desc, func, select

from app.core.config import settings
from app.core.dependencies import CurrentUser, DbSession
from app.models.assumption import Assumption
from app.models.attack_forecast import AttackForecast
from app.models.device import Device
from app.models.network_traffic import NetworkTraffic
from app.models.security_event import SecurityEvent
from app.models.telemetry import TelemetrySample
from app.services.ml_forecasting_service import model_status
from app.services.traffic_analyzer import all_user_flows
from app.utils.helpers import utc_now

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(current_user: CurrentUser, db: DbSession) -> dict:
    event_count = db.scalar(select(func.count(SecurityEvent.id)).where(SecurityEvent.user_id == current_user.id)) or 0
    flow_count = db.scalar(select(func.count(NetworkTraffic.id)).where(NetworkTraffic.user_id == current_user.id)) or 0
    forecast_count = db.scalar(select(func.count(AttackForecast.id)).where(AttackForecast.user_id == current_user.id)) or 0
    assumption_count = db.scalar(select(func.count(Assumption.id)).where(Assumption.user_id == current_user.id)) or 0
    device_count = db.scalar(select(func.count(Device.id)).where(Device.user_id == current_user.id)) or 0
    active_devices = db.scalar(select(func.count(Device.id)).where(Device.user_id == current_user.id, Device.authorization_state == "ACTIVE")) or 0
    authorized_devices = db.scalar(select(func.count(Device.id)).where(Device.user_id == current_user.id, Device.authorization_state.in_(["AUTHORIZED", "ACTIVE"]))) or 0
    now = utc_now()
    freshness_limit = timedelta(seconds=settings.collector_stale_seconds)
    active_records = db.scalars(select(Device).where(Device.user_id == current_user.id, Device.authorization_state == "ACTIVE")).all()
    online_devices = sum(1 for device in active_records if device.last_telemetry_at and now - device.last_telemetry_at <= freshness_limit)
    stale_devices = sum(1 for device in active_records if device.last_telemetry_at and freshness_limit < now - device.last_telemetry_at <= freshness_limit * 2)
    offline_devices = len(active_records) - online_devices - stale_devices
    return {"events_processed": event_count, "flows_processed": flow_count, "forecasts_generated": forecast_count, "assumptions_tracked": assumption_count, "devices": {"total": device_count, "active": active_devices, "authorized": authorized_devices, "online": online_devices, "stale": stale_devices, "offline": offline_devices}, "data_source": "REAL", "model": model_status()}


@router.get("/timeline")
def timeline(current_user: CurrentUser, db: DbSession, limit: int = 100) -> list[dict]:
    events = db.scalars(select(SecurityEvent).where(SecurityEvent.user_id == current_user.id).order_by(SecurityEvent.timestamp.desc()).limit(min(limit, 500))).all()
    return [{"timestamp": event.timestamp, "type": "SECURITY_EVENT", "id": event.id, "risk_score": round(100 - event.integrity_score, 2), "decision": event.decision, "conflicts": event.detected_conflicts, "evidence": event.explanation, "data_source": "REAL"} for event in events]


@router.get("/risk")
def risk(current_user: CurrentUser, db: DbSession) -> dict:
    event = db.scalar(select(SecurityEvent).where(SecurityEvent.user_id == current_user.id).order_by(SecurityEvent.timestamp.desc()))
    return {"risk_score": round(100 - event.integrity_score, 2) if event else 0.0, "decision": event.decision if event else "PASS", "conflicts": event.detected_conflicts if event else [], "data_source": "REAL", "telemetry_available": event is not None}


@router.get("/attack-path")
def attack_path(current_user: CurrentUser, db: DbSession) -> dict:
    forecast = db.scalar(select(AttackForecast).where(AttackForecast.user_id == current_user.id).order_by(AttackForecast.created_at.desc()))
    return forecast.attack_path if forecast else {"attack_path_detected": False, "predicted_path": [], "path_risk_score": 0.0, "reasoning": []}


@router.get("/relationships")
def relationships(current_user: CurrentUser, db: DbSession) -> list[dict]:
    flows = all_user_flows(db, current_user.id)
    return [{"source": flow.source_entity, "destination": flow.destination_entity, "port": flow.destination_port, "protocol": flow.protocol, "timestamp": flow.timestamp, "risk": 100 - float((flow.derived_features or {}).get("relationship_score", 50))} for flow in flows[:500]]


@router.get("/assumptions")
def assumptions(current_user: CurrentUser, db: DbSession) -> list[dict]:
    records = db.scalars(select(Assumption).where(Assumption.user_id == current_user.id).order_by(Assumption.last_observed.desc()).limit(500)).all()
    return [{"id": record.id, "type": record.assumption_type, "reference": record.value_hash_or_reference, "confidence": record.confidence, "risk_weight": record.risk_weight, "status": record.status, "supporting_events": record.supporting_events, "contradicting_events": record.contradicting_events, "first_verified": record.first_verified, "expires_at": record.expires_at, "last_verified": record.last_observed} for record in records]


@router.get("/live-events")
def live_events(current_user: CurrentUser, db: DbSession) -> list[dict]:
    return timeline(current_user, db, limit=20)


@router.get("/telemetry")
def telemetry(current_user: CurrentUser, db: DbSession, limit: int = 100) -> list[dict]:
    samples = db.scalars(select(TelemetrySample).where(TelemetrySample.user_id == current_user.id).order_by(TelemetrySample.timestamp.desc()).limit(min(limit, 500))).all()
    return [{"id": sample.id, "device_id": sample.device_id, "timestamp": sample.timestamp, "received_at": sample.received_at, "cpu_percent": sample.cpu_percent, "memory_percent": sample.memory_percent, "disk_percent": sample.disk_percent, "uptime_seconds": sample.uptime_seconds, "bytes_sent": sample.bytes_sent, "bytes_received": sample.bytes_received, "connection_count": sample.connection_count, "data_source": sample.data_source} for sample in samples]
