from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.core.dependencies import CurrentUser, DbSession
from app.core.rate_limit import security_rate_limit
from app.models.attack_forecast import AttackForecast
from app.models.device import Device
from app.schemas.demo import DemoRequest, DemoResponse
from app.schemas.network_traffic import ForecastRead, NetworkAnalysisResponse, NetworkBaselineRead, NetworkTrafficCreate, NetworkTrafficRead
from app.services.decision_engine import decide
from app.services.explanation_engine import explain
from app.services.forecasting_engine import forecast
from app.services.integrity_engine import calculate_network_integrity
from app.services.network_baseline_service import build_baseline
from app.services.traffic_analyzer import all_user_flows, baseline_update_allowed, persist_flow, record_flow, user_flows
from app.utils.helpers import hash_identifier, utc_now
from app.services.demo_data_service import DEMO_LABEL, build_demo_flows
from app.services.response_recommendation_service import recommendations

router = APIRouter(prefix="/network", tags=["network"])
forecast_router = APIRouter(prefix="/security", tags=["security"], dependencies=[Depends(security_rate_limit)])


def _authorized_device(payload: NetworkTrafficCreate, current_user: CurrentUser, db: DbSession) -> Device | None:
    if not payload.device_id:
        return None
    device = db.scalar(select(Device).where(Device.id == payload.device_id, Device.user_id == current_user.id))
    if device is None:
        raise HTTPException(status_code=404, detail="Authorized device not found")
    if device.authorization_state != "ACTIVE":
        raise HTTPException(status_code=403, detail=f"Device monitoring is {device.authorization_state}; telemetry collection is denied")
    return device


def _record_device_heartbeat(device: Device, timestamp) -> None:
    observed_at = timestamp or utc_now()
    device.last_telemetry_at = observed_at
    device.last_seen = observed_at
    device.status = "ONLINE"


@router.post("/traffic", response_model=NetworkTrafficRead)
def traffic(payload: NetworkTrafficCreate, current_user: CurrentUser, db: DbSession):
    device = _authorized_device(payload, current_user, db)
    historical_count = len(user_flows(db, current_user.id))
    from app.services.event_ingestion_service import ingest_flow
    flow, duplicate = ingest_flow(db, current_user.id, payload)
    flow.device_id = device.id if device else None
    if device:
        _record_device_heartbeat(device, flow.timestamp)
    analysis = {"relationship_score": flow.derived_features.get("relationship_score", 0.0)}
    features = {key: value for key, value in flow.derived_features.items() if key not in {"conflicts", "relationship_score", "relationship_deltas"}}
    conflicts = flow.derived_features.get("conflicts", [])
    integrity = calculate_network_integrity(analysis["relationship_score"], features, conflicts)
    eligible = not duplicate and baseline_update_allowed(integrity.score, integrity.conflicts, historical_count)
    if not duplicate:
        from app.services.assumption_service import update_relationship_assumption
        update_relationship_assumption(db, current_user.id, f"{flow.destination_entity}:{flow.protocol}:{flow.destination_port}", True, bool(integrity.conflicts))
    persisted = persist_flow(db, flow, eligible)
    return NetworkTrafficRead(id=persisted.id, device_id=persisted.device_id, timestamp=persisted.timestamp, source_entity=persisted.source_entity, destination_entity=persisted.destination_entity, protocol=persisted.protocol, destination_port=persisted.destination_port, derived_features=persisted.derived_features, baseline_eligible=eligible, event_fingerprint=persisted.event_fingerprint, is_duplicate=duplicate)


@router.post("/analyze")
def analyze_network(payload: NetworkTrafficCreate, current_user: CurrentUser, db: DbSession) -> NetworkAnalysisResponse:
    device = _authorized_device(payload, current_user, db)
    historical = user_flows(db, current_user.id)
    from app.services.event_ingestion_service import ingest_flow
    flow, duplicate = ingest_flow(db, current_user.id, payload)
    flow.device_id = device.id if device else None
    if device:
        _record_device_heartbeat(device, flow.timestamp)
    analysis = {"relationship_score": flow.derived_features.get("relationship_score", 0.0)}
    features = {key: value for key, value in flow.derived_features.items() if key not in {"conflicts", "relationship_score", "relationship_deltas"}}
    conflicts = flow.derived_features.get("conflicts", [])
    integrity = calculate_network_integrity(analysis["relationship_score"], features, conflicts)
    flows = [*historical] if duplicate else [*historical, flow]
    result = forecast(flows, integrity.conflicts, analysis["relationship_score"], integrity.score, baseline_flows=historical)
    decision = decide(integrity.score, integrity.conflicts)
    explanation = explain(decision.decision, integrity.conflicts, "ADMIN")
    explanation["forecast"] = {"type": result["predicted_attack_type"], "probability": result["attack_probability"], "confidence": result["confidence"]}
    explanation["forecast_evidence"] = {"source": result["forecast_source"], "ml_confidence": result["ml_confidence_level"], "evidence": result["evidence"], "hybrid_weights": result["hybrid_weights"]}
    explanation["recommended_actions"] = recommendations(decision.decision.value, integrity.conflicts, result)
    eligible = not duplicate and baseline_update_allowed(integrity.score, integrity.conflicts, len(historical))
    persisted = persist_flow(db, flow, eligible)
    from app.services.assumption_service import update_relationship_assumption
    if not duplicate:
        update_relationship_assumption(db, current_user.id, f"{flow.destination_entity}:{flow.protocol}:{flow.destination_port}", True, bool(integrity.conflicts))
    from app.models.security_event import SecurityEvent
    db.add(SecurityEvent(user_id=current_user.id, integrity_score=integrity.score, decision=decision.decision.value, signal_scores=integrity.signal_scores, detected_conflicts=integrity.conflicts, explanation=explanation))
    db.commit()
    return NetworkAnalysisResponse(flow_id=persisted.id, features={**features, "duplicate_event": duplicate, "relationship_deltas": flow.derived_features.get("relationship_deltas", {})}, integrity_score=integrity.score, signal_scores=integrity.signal_scores, relationship_score=analysis["relationship_score"], conflicts=integrity.conflicts, decision=decision.decision.value, baseline_eligible=eligible, forecast=result)


@router.get("/baseline/{entity_id}", response_model=NetworkBaselineRead, responses={404: {"description": "Network baseline not found"}})
def baseline(entity_id: str, current_user: CurrentUser, db: DbSession):
    flows = user_flows(db, current_user.id)
    if not flows:
        raise HTTPException(status_code=404, detail="Network baseline not found")
    return NetworkBaselineRead(entity_id=entity_id, baseline=build_baseline(flows, hash_identifier(entity_id)))


@router.post("/demo", response_model=DemoResponse)
def demo(payload: DemoRequest) -> DemoResponse:
    return DemoResponse(label=DEMO_LABEL, scenario=payload.scenario, flows=[flow.model_dump(exclude_none=True) for flow in build_demo_flows(payload.scenario)])


@forecast_router.post("/forecast", response_model=ForecastRead)
def create_forecast(current_user: CurrentUser, db: DbSession):
    flows = all_user_flows(db, current_user.id)
    result = forecast(flows)
    if not flows:
        return {"id": str(uuid4()), **result, "created_at": utc_now()}
    record = AttackForecast(user_id=current_user.id, event_ids=[flow.id for flow in flows], forecast_available=result["forecast_available"], forecast_source=result["forecast_source"], predicted_attack_type=result["predicted_attack_type"], attack_probability=result["attack_probability"], confidence=result["confidence"], potential_targets=result["potential_targets"], risk_level=result["risk_level"], reasoning=result["reasoning"], ml_probabilities=result["ml_probabilities"], sequence_analysis=result["sequence_analysis"], hybrid_weights=result["hybrid_weights"], evidence=result["evidence"], ml_confidence_level=result["ml_confidence_level"], attack_path=result["attack_path"], attack_stage_probabilities=result["attack_stage_probabilities"], attack_stage_evidence=result["attack_stage_evidence"], contributing_signals=result["contributing_signals"], multi_window_analysis=result["multi_window_analysis"])
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, **result, "created_at": record.created_at}


@forecast_router.get("/forecast/{forecast_id}", response_model=ForecastRead, responses={404: {"description": "Forecast not found"}})
def get_forecast(forecast_id: str, current_user: CurrentUser, db: DbSession):
    record = db.scalar(select(AttackForecast).where(AttackForecast.id == forecast_id, AttackForecast.user_id == current_user.id))
    if record is None:
        raise HTTPException(status_code=404, detail="Forecast not found")
    return {"id": record.id, "forecast_available": record.forecast_available, "forecast_source": record.forecast_source, "ml_model_loaded": record.forecast_source == "ML_MODEL", "predicted_attack_type": record.predicted_attack_type, "attack_probability": record.attack_probability, "confidence": record.confidence, "potential_targets": record.potential_targets, "risk_level": record.risk_level, "reasoning": record.reasoning, "ml_probabilities": record.ml_probabilities, "sequence_analysis": record.sequence_analysis, "hybrid_weights": record.hybrid_weights, "evidence": record.evidence, "ml_confidence_level": record.ml_confidence_level, "attack_path": record.attack_path, "attack_stage_probabilities": record.attack_stage_probabilities, "attack_stage_evidence": record.attack_stage_evidence, "contributing_signals": record.contributing_signals, "multi_window_analysis": record.multi_window_analysis, "created_at": record.created_at}
