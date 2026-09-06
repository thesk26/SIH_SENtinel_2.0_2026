from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assumption import Assumption
from app.models.assumption_transition import AssumptionTransition
from app.core.config import settings


def _transition(db: Session, assumption: Assumption, new_status: str, reason: str) -> None:
    if assumption.status == new_status:
        return
    db.add(AssumptionTransition(assumption_id=assumption.id, previous_status=assumption.status, new_status=new_status, reason=reason))
    assumption.status = new_status


def update_relationship_assumption(db: Session, user_id: str, reference: str, observed: bool, suspicious: bool) -> Assumption:
    assumption = db.scalar(select(Assumption).where(Assumption.user_id == user_id, Assumption.value_hash_or_reference == reference, Assumption.assumption_type == "RELATIONSHIP"))
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if assumption is None:
        assumption = Assumption(user_id=user_id, assumption_type="RELATIONSHIP", value_hash_or_reference=reference, status="OBSERVED")
        db.add(assumption)
    if observed:
        if suspicious:
            assumption.contradicting_events = (assumption.contradicting_events or 0) + 1
        else:
            assumption.frequency = (assumption.frequency or 0) + 1
            assumption.supporting_events = (assumption.supporting_events or 0) + 1
        assumption.last_observed = now
        if not suspicious:
            assumption.confidence = min(1.0, (assumption.confidence or 0.0) + 0.05)
            if assumption.status == "OBSERVED" and assumption.supporting_events >= settings.assumption_candidate_events:
                _transition(db, assumption, "CANDIDATE", "Repeated behavior observed")
            elif assumption.status == "CANDIDATE" and assumption.supporting_events >= settings.assumption_learning_events:
                _transition(db, assumption, "LEARNING", "Behavior entered verification period")
            elif assumption.status == "LEARNING" and assumption.confidence >= settings.assumption_trust_confidence and assumption.supporting_events >= settings.assumption_trust_events:
                _transition(db, assumption, "TRUSTED", "Sufficient consistent evidence accumulated")
            elif assumption.status == "WEAKENED" and assumption.confidence >= settings.assumption_trust_confidence:
                _transition(db, assumption, "LEARNING", "Consistent evidence supports recovery")
            if assumption.status == "EXPIRED":
                _transition(db, assumption, "RETIRED", "Expired assumption remained inactive")
                assumption.first_verified = assumption.first_verified or now
        elif assumption.status == "TRUSTED":
            assumption.confidence = max(0.0, (assumption.confidence or 0.0) - 0.1)
            _transition(db, assumption, "WEAKENED", "Contradictory evidence reduced confidence")
        assumption.expires_at = now + timedelta(days=settings.assumption_expiry_days)
    if assumption.expires_at and assumption.expires_at < now and assumption.status not in {"RETIRED", "EXPIRED"}:
        assumption.status = "EXPIRED"
    if assumption.status == "EXPIRED" and not observed:
        assumption.status = "RETIRED"
    return assumption


def expire_assumption(db: Session, assumption: Assumption) -> Assumption:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if assumption.expires_at and assumption.expires_at < now and assumption.status not in {"EXPIRED", "RETIRED"}:
        _transition(db, assumption, "EXPIRED", "Verification period elapsed")
    return assumption
