import hashlib
import json

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.core.dependencies import CurrentUser, DbSession
from app.models.audit import AuditLog, EvidenceArtifact
from app.models.device import Device
from app.schemas.response import EvidenceRead, EvidenceRequest, ResponseActionRead, ResponseActionRequest
from app.utils.helpers import utc_now

router = APIRouter(prefix="/response", tags=["response"])


def _device(device_id: str | None, current_user: CurrentUser, db: DbSession) -> Device | None:
    if not device_id:
        return None
    device = db.scalar(select(Device).where(Device.id == device_id, Device.user_id == current_user.id))
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/actions", response_model=ResponseActionRead)
def request_action(payload: ResponseActionRequest, current_user: CurrentUser, db: DbSession):
    device = _device(payload.device_id, current_user, db)
    if device and payload.action.upper() in {"ISOLATE", "QUARANTINE", "SCAN"} and device.authorization_state != "ACTIVE":
        raise HTTPException(status_code=403, detail="Response action requires an ACTIVE authorized device")
    audit = AuditLog(user_id=current_user.id, device_id=device.id if device else None, event_type="RESPONSE_ACTION", action=payload.action.upper(), status="SIMULATED", details={"reason": payload.reason, "incident_id": payload.incident_id}, data_source="REAL")
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return {"id": audit.id, "action": audit.action, "device_id": audit.device_id, "status": audit.status, "mode": "SIMULATION", "timestamp": audit.timestamp, "audit_id": audit.id}


@router.post("/evidence", response_model=EvidenceRead)
def preserve_evidence(payload: EvidenceRequest, current_user: CurrentUser, db: DbSession):
    device = _device(payload.device_id, current_user, db)
    serialized = json.dumps(payload.evidence, sort_keys=True, separators=(",", ":"))
    artifact = EvidenceArtifact(user_id=current_user.id, device_id=device.id if device else None, event_id=payload.event_id, evidence_hash=hashlib.sha256(serialized.encode()).hexdigest(), evidence=payload.evidence, data_source="REAL", timestamp=utc_now())
    db.add(artifact)
    db.add(AuditLog(user_id=current_user.id, device_id=device.id if device else None, event_type="EVIDENCE_PRESERVED", action="PRESERVE", status="RECORDED", details={"evidence_id": artifact.id}, data_source="REAL"))
    db.commit()
    db.refresh(artifact)
    return artifact
