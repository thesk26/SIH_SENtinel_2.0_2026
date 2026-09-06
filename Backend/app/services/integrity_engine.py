from dataclasses import dataclass

from app.schemas.security import SecurityAnalyzeRequest
from app.utils.helpers import clamp, hash_identifier


@dataclass(frozen=True)
class IntegrityResult:
    score: float
    signal_scores: dict[str, float]
    conflicts: list[str]


def calculate_network_integrity(relationship_score: float, features: dict, conflicts: list[str]) -> IntegrityResult:
    traffic_score = 100.0
    if features.get("traffic_spike"):
        traffic_score -= 30.0
    if features.get("rapid_connections"):
        traffic_score -= 20.0
    traffic_score -= min(30.0, float(features.get("repeated_failures", 0)) * 5.0)
    temporal_score = 70.0 if features.get("rapid_connections") else 100.0
    scores = {"traffic": clamp(traffic_score), "relationship": clamp(relationship_score), "temporal": temporal_score}
    weights = {"traffic": 1.5, "relationship": 1.4, "temporal": 0.8}
    dynamic_weights: dict[str, float] = {}
    for name, score in scores.items():
        base_weight = weights.get(name, 1.0)
        dynamic_weights[name] = base_weight * (1.35 if score < 60 else 1.0)
    score = sum(scores[name] * dynamic_weights[name] for name in scores) / sum(dynamic_weights.values())
    unique_conflicts = len(set(conflicts))
    if unique_conflicts >= 2:
        score -= min(30.0, (unique_conflicts - 1) * 8.0)
    return IntegrityResult(round(clamp(score), 2), {name: round(value, 2) for name, value in scores.items()}, list(dict.fromkeys(conflicts)))


def _deviation_score(current: float | None, expected: float | None, tolerance: float) -> float:
    if current is None or expected is None:
        return 70.0
    return clamp(100.0 - abs(current - expected) / max(abs(expected), tolerance) * 100.0)


def _behavior_score(request: SecurityAnalyzeRequest, baseline_data: dict) -> float:
    values = (("typing_speed", 10.0), ("key_press_mean_ms", 20.0), ("mouse_speed", 10.0), ("click_frequency", 2.0))
    return sum(_deviation_score(getattr(request, field), baseline_data.get(field), tolerance) for field, tolerance in values) / len(values)


def _device_score(request: SecurityAnalyzeRequest, baseline_data: dict) -> tuple[float, list[str]]:
    known_devices = set(baseline_data.get("known_devices", []))
    device_hash = hash_identifier(request.device_fingerprint)
    if device_hash and device_hash in known_devices:
        return 100.0, []
    return 45.0, ["NEW_DEVICE"] if device_hash else []


def _location_score(request: SecurityAnalyzeRequest, baseline_data: dict) -> tuple[float, list[str]]:
    known_regions = set(baseline_data.get("known_regions", []))
    if not request.region:
        return 55.0, []
    if request.region in known_regions:
        return 100.0, []
    return 40.0, ["UNUSUAL_LOCATION"]


def _network_score(request: SecurityAnalyzeRequest) -> tuple[float, list[str]]:
    score = clamp(request.ip_reputation_score - (30.0 if request.is_vpn_or_proxy else 0.0) - (20.0 if request.network_changed else 0.0))
    return score, ["SUSPICIOUS_NETWORK"] if score < 55 else []


def _time_score(request: SecurityAnalyzeRequest, baseline_data: dict) -> tuple[float, list[str]]:
    score = _deviation_score(request.login_hour, baseline_data.get("login_hour"), 4.0)
    return score, ["UNUSUAL_TIME"] if score < 55 else []


def calculate_integrity(request: SecurityAnalyzeRequest, baseline_data: dict, relationship_score: float | None = None) -> IntegrityResult:
    device_score, conflicts = _device_score(request, baseline_data)
    location_score, location_conflicts = _location_score(request, baseline_data)
    network_score, network_conflicts = _network_score(request)
    time_score, time_conflicts = _time_score(request, baseline_data)
    scores: dict[str, float] = {"device": device_score, "location": location_score, "network": network_score, "time": time_score}
    conflicts.extend(location_conflicts + network_conflicts + time_conflicts)
    scores["behavior"] = _behavior_score(request, baseline_data)
    if scores["behavior"] < 55:
        conflicts.append("ABNORMAL_BEHAVIOR")
    scores["relationship"] = clamp(relationship_score if relationship_score is not None else baseline_data.get("relationship_score", 50.0))

    base_weights = {"device": 1.2, "behavior": 1.4, "location": 1.1, "network": 1.5, "time": 0.8, "relationship": 1.0}
    dynamic_weights: dict[str, float] = {}
    for name, score in scores.items():
        base_weight = base_weights.get(name, 1.0)
        dynamic_weights[name] = base_weight * (1.35 if score < 60 else 1.0)
    weighted = sum(scores[name] * dynamic_weights[name] for name in scores)
    total_weight = sum(dynamic_weights.values())
    score = weighted / total_weight
    significant_count = len(set(conflicts))
    if significant_count >= 2:
        score -= min(30.0, (significant_count - 1) * 8.0)
        conflicts.append("MULTI_SIGNAL_CONFLICT")
    if significant_count >= 4:
        conflicts.append("MULTI_SIGNAL_CRITICAL")
    return IntegrityResult(round(clamp(score), 2), {key: round(value, 2) for key, value in scores.items()}, conflicts)
