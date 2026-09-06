from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.core.dependencies import CurrentUser, DbSession
from app.core.rate_limit import security_rate_limit
from app.models.security_event import SecurityEvent
from app.schemas.security import SecurityAnalysisResponse, SecurityAnalyzeRequest, SecurityEventRead
from app.services.decision_engine import decide
from app.services.explanation_engine import explain
from app.services.integrity_engine import calculate_integrity

router = APIRouter(prefix="/security", tags=["security"], dependencies=[Depends(security_rate_limit)])


def _response(event: SecurityEvent) -> SecurityEventRead:
    return SecurityEventRead(id=event.id, user_id=event.user_id, timestamp=event.timestamp, integrity_score=event.integrity_score, decision=event.decision, signal_scores=event.signal_scores, conflicts_detected=event.detected_conflicts, explanation=event.explanation)


@router.post("/analyze")
def analyze(payload: SecurityAnalyzeRequest, current_user: CurrentUser, db: DbSession) -> SecurityAnalysisResponse:
    from app.services.behavior_service import get_baseline
    baseline = get_baseline(db, current_user.id)
    baseline_data = baseline.statistical_data if baseline else {}
    result = calculate_integrity(payload, baseline_data)
    decision = decide(result.score, result.conflicts)
    explanation = explain(decision.decision, result.conflicts, payload.requested_explanation_level.value)
    event = SecurityEvent(user_id=current_user.id, integrity_score=result.score, decision=decision.decision.value, signal_scores=result.signal_scores, detected_conflicts=result.conflicts, explanation=explanation)
    db.add(event)
    db.commit()
    return SecurityAnalysisResponse(user_id=current_user.id, integrity_score=result.score, decision=decision.decision.value, signal_scores=result.signal_scores, conflicts_detected=result.conflicts, explanation=explanation)


@router.get("/events")
def events(current_user: CurrentUser, db: DbSession) -> list[SecurityEventRead]:
    records = db.scalars(select(SecurityEvent).where(SecurityEvent.user_id == current_user.id).order_by(SecurityEvent.timestamp.desc()).limit(100)).all()
    return [_response(record) for record in records]


@router.get("/events/{event_id}", responses={404: {"description": "Security event not found"}})
def event(event_id: str, current_user: CurrentUser, db: DbSession) -> SecurityEventRead:
    record = db.get(SecurityEvent, event_id)
    if record is None or (record.user_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=404, detail="Security event not found")
    return _response(record)
