from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbSession
from app.schemas.behavior import BaselineRead, BehaviorCollect
from app.services.behavior_service import collect_behavior, get_baseline

router = APIRouter(prefix="/behavior", tags=["behavior"])


@router.post("/collect")
def collect(payload: BehaviorCollect, current_user: CurrentUser, db: DbSession) -> BaselineRead:
    baseline = collect_behavior(db, current_user.id, payload)
    return BaselineRead(user_id=current_user.id, baseline_type=baseline.baseline_type, statistical_data=baseline.statistical_data, confidence=baseline.confidence, updated_at=baseline.updated_at)


@router.get("/baseline/{user_id}", responses={403: {"description": "Not authorized"}, 404: {"description": "Baseline not found"}})
def baseline(user_id: str, current_user: CurrentUser, db: DbSession) -> BaselineRead:
    if user_id != current_user.id and current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized to view this baseline")
    record = get_baseline(db, user_id)
    if record is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Baseline not found")
    return BaselineRead(user_id=user_id, baseline_type=record.baseline_type, statistical_data=record.statistical_data, confidence=record.confidence, updated_at=record.updated_at)
