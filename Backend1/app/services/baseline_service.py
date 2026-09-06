from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.behavior import BehavioralBaseline, BehaviorSample
from app.schemas.behavior import BehaviorCollect
from app.utils.helpers import hash_identifier, utc_now


FIELDS = ("typing_speed", "key_press_mean_ms", "key_release_mean_ms", "mouse_speed", "mouse_acceleration", "click_frequency", "session_duration_seconds", "login_hour")


def update_baseline(db: Session, user_id: str, sample: BehaviorCollect) -> BehavioralBaseline:
    values = sample.model_dump()
    values["device_fingerprint_hash"] = hash_identifier(values.pop("device_fingerprint", None))
    values["network_hash"] = hash_identifier(values.pop("network_identifier", None))
    db.add(BehaviorSample(user_id=user_id, **values))
    baseline = db.scalar(select(BehavioralBaseline).where(BehavioralBaseline.user_id == user_id))
    rows = list(db.scalars(select(BehaviorSample).where(BehaviorSample.user_id == user_id).order_by(BehaviorSample.created_at.desc()).limit(200)))
    if baseline is None:
        baseline = BehavioralBaseline(user_id=user_id)
        db.add(baseline)
    data: dict = {}
    for field in FIELDS:
        numbers = [getattr(row, field) for row in rows if getattr(row, field) is not None]
        if numbers:
            recent_weighted = sum(value * (len(numbers) - index) for index, value in enumerate(numbers))
            divisor = sum(range(1, len(numbers) + 1))
            data[field] = recent_weighted / divisor
    data["known_devices"] = list({row.device_fingerprint_hash for row in rows if row.device_fingerprint_hash})
    data["known_regions"] = list({row.region for row in rows if row.region})
    data["known_networks"] = list({row.network_hash for row in rows if row.network_hash})
    baseline.statistical_data = data
    if rows:
        timestamps = [row.created_at for row in rows]
        span_days = max(0.0, (max(timestamps) - min(timestamps)).total_seconds() / 86400)
        quantity = min(1.0, len(rows) / max(20, settings.baseline_days * 4))
        coverage = min(1.0, span_days / max(1, settings.baseline_days))
        devices = [row.device_fingerprint_hash for row in rows if row.device_fingerprint_hash]
        consistency = max(Counter(devices).values()) / len(devices) if devices else 0.5
        baseline.confidence = round(min(1.0, quantity * 0.4 + coverage * 0.3 + consistency * 0.3), 3)
    else:
        baseline.confidence = 0.0
    baseline.updated_at = utc_now()
    db.commit()
    db.refresh(baseline)
    return baseline
