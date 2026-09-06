from __future__ import annotations

from app.core.config import settings


def adaptive_weights(*, ml_available: bool, ml_confidence_level: str, sequence_available: bool, relationship_available: bool, integrity_available: bool) -> dict[str, float]:
    candidates = {
        "ml": settings.ml_forecast_weight * {"HIGH": 1.0, "MEDIUM": 0.7, "LOW": 0.35}.get(ml_confidence_level, 0.35) if ml_available else 0.0,
        "sequence": settings.sequence_analysis_weight if sequence_available else 0.0,
        "relationship": settings.relationship_analysis_weight if relationship_available else 0.0,
        "integrity": settings.integrity_analysis_weight if integrity_available else 0.0,
    }
    total = sum(candidates.values())
    if total <= 0:
        return {name: 0.0 for name in candidates}
    return {name: round(weight / total, 6) for name, weight in candidates.items()}
