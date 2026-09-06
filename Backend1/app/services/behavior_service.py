from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.behavior import BehavioralBaseline
from app.schemas.behavior import BehaviorCollect
from app.services.baseline_service import update_baseline


def collect_behavior(db: Session, user_id: str, sample: BehaviorCollect) -> BehavioralBaseline:
    return update_baseline(db, user_id, sample)


def get_baseline(db: Session, user_id: str) -> BehavioralBaseline | None:
    return db.scalar(select(BehavioralBaseline).where(BehavioralBaseline.user_id == user_id))
