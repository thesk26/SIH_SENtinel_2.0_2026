from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import func, select

from app.core.dependencies import CurrentUser, DbSession
from app.models.assumption import Assumption
from app.models.attack_forecast import AttackForecast
from app.models.network_traffic import NetworkTraffic
from app.models.security_event import SecurityEvent
from app.services.ml_forecasting_service import model_status
from app.services.traffic_analyzer import all_user_flows

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(current_user: CurrentUser, db: DbSession) -> dict:
    event_count = db.scalar(select(func.count(SecurityEvent.id)).where(SecurityEvent.user_id == current_user.id)) or 0
    flow_count = db.scalar(select(func.count(NetworkTraffic.id)).where(NetworkTraffic.user_id == current_user.id)) or 0
    forecast_count = db.scalar(select(func.count(AttackForecast.id)).where(AttackForecast.user_id == current_user.id)) or 0
    assumption_count = db.scalar(select(func.count(Assumption.id)).where(Assumption.user_id == current_user.id)) or 0
    return {"events_processed": event_count, "flows_processed": flow_count, "forecasts_generated": forecast_count, "assumptions_tracked": assumption_count, "model": model_status()}


@router.get("/timeline")
def timeline(current_user: CurrentUser, db: DbSession, limit: int = 100) -> list[dict]:
    events = db.scalars(select(SecurityEvent).where(SecurityEvent.user_id == current_user.id).order_by(SecurityEvent.timestamp.desc()).limit(min(limit, 500))).all()
    return [{"timestamp": event.timestamp, "type": "SECURITY_EVENT", "id": event.id, "risk_score": round(100 - event.integrity_score, 2), "decision": event.decision, "conflicts": event.detected_conflicts, "evidence": event.explanation} for event in events]


@router.get("/risk")
def risk(current_user: CurrentUser, db: DbSession) -> dict:
    event = db.scalar(select(SecurityEvent).where(SecurityEvent.user_id == current_user.id).order_by(SecurityEvent.timestamp.desc()))
    return {"risk_score": round(100 - event.integrity_score, 2) if event else 0.0, "decision": event.decision if event else "PASS", "conflicts": event.detected_conflicts if event else []}


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
