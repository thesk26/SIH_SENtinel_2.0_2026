from collections import defaultdict
from typing import Iterable

from app.core.config import settings


CRITICAL_PORTS = {22, 23, 445, 3389, 5432, 3306, 1433, 6379}


def _score_target(entity_flows: list, suspicious_conflicts: set[str]) -> dict:
    reasons: list[str] = []
    relationship_anomaly = 55.0 if "NEW_RELATIONSHIP" in suspicious_conflicts else 10.0
    traffic_anomaly = 0.0
    criticality = 0.0
    for flow in entity_flows:
        features = flow.derived_features or {}
        flow_conflicts = set(features.get("conflicts", []))
        if "NEW_RELATIONSHIP" in flow_conflicts:
            relationship_anomaly = max(relationship_anomaly, 55.0)
            reasons.append("New relationship")
        if features.get("traffic_spike"):
            traffic_anomaly = max(traffic_anomaly, 30.0)
            reasons.append("Traffic spike")
        if features.get("rapid_connections") or features.get("repeated_failures", 0) >= 3:
            traffic_anomaly = max(traffic_anomaly, 20.0)
        if flow.destination_port in CRITICAL_PORTS:
            criticality = max(criticality, 20.0)
            reasons.append("Critical service port")
    frequency = len(entity_flows)
    frequency_score = min(20.0, frequency * 4.0) if frequency >= 3 else frequency * 3.0
    if frequency >= 3:
        reasons.append("High suspicious connection frequency")
    score = min(100.0, relationship_anomaly + traffic_anomaly + criticality + frequency_score)
    return {"target_risk_score": round(score, 2), "reason": list(dict.fromkeys(reasons))}


def predict_targets(flows: Iterable, conflicts: list[str] | None = None) -> list[dict]:
    grouped: dict[str, list] = defaultdict(list)
    for flow in flows:
        grouped[flow.destination_entity].append(flow)
    suspicious_conflicts = set(conflicts or [])
    predictions = []
    for entity, entity_flows in grouped.items():
        prediction = _score_target(entity_flows, suspicious_conflicts)
        if prediction["target_risk_score"] >= 45.0:
            predictions.append({"entity": entity, **prediction})
    return sorted(predictions, key=lambda item: item["target_risk_score"], reverse=True)[: settings.max_predicted_targets]
