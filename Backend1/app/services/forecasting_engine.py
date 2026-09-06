from app.core.config import settings
from app.services.attack_sequence_analyzer import analyze_sequence
from app.services.attack_path_service import predict_attack_path
from app.services.attack_stage_service import stage_evidence, stage_probabilities
from app.services.hybrid_weight_service import adaptive_weights
from app.services.ml_forecasting_service import predict
from app.services.target_prediction_service import predict_targets
from app.services.time_window_analyzer import aggregate_window


SEQUENCE_TO_CLASS = {
    "POSSIBLE_RECONNAISSANCE": "PORT_SCAN",
    "POSSIBLE_BRUTE_FORCE": "BRUTE_FORCE",
    "POSSIBLE_LATERAL_MOVEMENT": "LATERAL_MOVEMENT",
    "POSSIBLE_DATA_EXFILTRATION": "DATA_EXFILTRATION",
}


def _aggregate_features(flows: list, baseline_flows: list | None = None) -> dict:
    return aggregate_window(flows, settings.default_analysis_window_minutes, baseline_flows=baseline_flows)


def _rule_scores(conflicts: set[str], sequence: dict, sequence_class: str | None) -> dict[str, float]:
    scores = dict.fromkeys(("NORMAL", "PORT_SCAN", "BRUTE_FORCE", "LATERAL_MOVEMENT", "DOS_OR_DDOS", "DATA_EXFILTRATION"), 0.0)
    scores["NORMAL"] = 0.85 if not conflicts else 0.15
    if sequence_class:
        scores[sequence_class] = max(scores[sequence_class], sequence["sequence_confidence"])
    if "TRAFFIC_SPIKE" in conflicts:
        scores["DOS_OR_DDOS"] = max(scores["DOS_OR_DDOS"], 0.65)
    if "NEW_RELATIONSHIP" in conflicts:
        scores["LATERAL_MOVEMENT"] = max(scores["LATERAL_MOVEMENT"], 0.75)
    return scores


def _combine_scores(rule_scores: dict[str, float], probabilities: dict[str, float], sequence: dict, sequence_class: str | None, relationship_score: float | None, integrity_score: float | None, ml_result: dict) -> tuple[dict[str, float], dict[str, float]]:
    weights = adaptive_weights(ml_available=ml_result["available"], ml_confidence_level=ml_result["confidence_level"], sequence_available=True, relationship_available=relationship_score is not None, integrity_available=integrity_score is not None)
    combined: dict[str, float] = {}
    for class_name, rule_score in rule_scores.items():
        sequence_score = sequence["sequence_confidence"] if class_name == sequence_class else 0.0
        anomaly_signal = max(0.0, min(1.0, (100.0 - relationship_score) / 100.0)) if relationship_score is not None else 0.0
        normal_relationship = min(1.0, relationship_score / 100.0) if relationship_score is not None else 0.0
        integrity_signal = max(0.0, min(1.0, (100.0 - integrity_score) / 100.0)) if integrity_score is not None else 0.0
        normal_integrity = min(1.0, integrity_score / 100.0) if integrity_score is not None else 0.0
        relationship_component = normal_relationship if class_name == "NORMAL" else anomaly_signal
        integrity_component = normal_integrity if class_name == "NORMAL" else integrity_signal
        combined[class_name] = probabilities.get(class_name, 0.0) * weights["ml"] + sequence_score * weights["sequence"] + relationship_component * weights["relationship"] + integrity_component * weights["integrity"] + rule_score * 0.1
    return combined, weights


def _risk_level(significant: int, probability: float) -> str:
    if significant >= 4 or probability >= 85:
        return "CRITICAL"
    if significant >= 3 or probability >= 65:
        return "HIGH"
    if significant >= 2:
        return "ELEVATED"
    return "LOW"


def forecast(flows: list, extra_conflicts: list[str] | None = None, relationship_score: float | None = None, integrity_score: float | None = None, baseline_flows: list | None = None) -> dict:
    if not flows:
        return {
            "forecast_available": False,
            "forecast_source": "RULE_BASED_FALLBACK",
            "ml_model_loaded": False,
            "predicted_attack_type": "NO_DATA",
            "attack_probability": None,
            "confidence": None,
            "potential_targets": [],
            "risk_level": "UNKNOWN",
            "reasoning": ["No network flows were available for forecasting"],
            "ml_probabilities": {},
            "sequence_analysis": analyze_sequence([]),
            "attack_path": {"attack_path_detected": False, "predicted_path": [], "path_edges": [], "selected_path_score": 0.0, "selected_path_reason": [], "global_environmental_context": {"overall_network_risk": 0.0, "unrelated_suspicious_events": 0}, "path_risk_score": 0.0, "reasoning": []},
            "attack_stage_probabilities": {},
            "attack_stage_evidence": {},
            "contributing_signals": [],
            "multi_window_analysis": {},
            "ml_confidence_level": "LOW",
            "ml_top_class": None,
            "ml_top_probability": 0.0,
            "hybrid_weights": {"ml": 0.0, "sequence": 1.0, "relationship": 0.0, "integrity": 0.0},
            "relationship_analysis_available": relationship_score is not None,
            "integrity_analysis_available": integrity_score is not None,
            "evidence": {"ml": {"available": False}, "sequence": {"detected": False}, "relationship": {"available": relationship_score is not None}, "integrity": {"available": integrity_score is not None}},
        }
    sequence = analyze_sequence(flows)
    multi_window = {str(window): aggregate_window(flows, window, baseline_flows=baseline_flows) for window in (settings.short_window_minutes, settings.medium_window_minutes, settings.long_window_minutes)}
    conflicts = set(extra_conflicts or [])
    conflicts.update(sequence["events"])
    ml_result = predict(_aggregate_features(flows, baseline_flows))
    probabilities = dict(ml_result["probabilities"])
    sequence_class = SEQUENCE_TO_CLASS.get(sequence["sequence_type"])
    rules = _rule_scores(conflicts, sequence, sequence_class)
    combined, effective_weights = _combine_scores(rules, probabilities, sequence, sequence_class, relationship_score, integrity_score, ml_result)
    predicted_class = max(combined, key=combined.get)
    probability = round(min(99.0, combined.get(predicted_class, 0.0) * 100.0), 2)
    significant = len(conflicts)
    targets = predict_targets(flows, list(conflicts))
    attack_path = predict_attack_path(flows, targets, sequence, baseline_flows=baseline_flows)
    attack_stages = stage_probabilities(sequence, ml_result["top_class"], ml_result["top_probability"])
    attack_stage_evidence = stage_evidence(sequence, ml_result["top_class"], ml_result["top_probability"])
    contribution_sources = {"ML_MODEL": effective_weights["ml"], "SEQUENCE_ANALYSIS": effective_weights["sequence"], "RELATIONSHIP_ANALYSIS": effective_weights["relationship"], "INTEGRITY_ANALYSIS": effective_weights["integrity"]}
    threat_match = any((flow.derived_features or {}).get("threat_intelligence", {}).get("matched") for flow in flows)
    reasoning = [f"{sequence['flow_count']} recent flow(s) evaluated", f"{len(conflicts)} related anomaly signal(s) observed"]
    if threat_match:
        reasoning.append("Local threat-intelligence evidence matched a reserved demonstration indicator")
    if ml_result["available"]:
        reasoning.append("ML model contributed class probabilities")
    else:
        reasoning.append("No trained ML artifact was available; rule-based fallback contributed the forecast")
    if sequence["sequence_detected"]:
        reasoning.append(f"The observed sequence matches {sequence['sequence_type'].replace('_', ' ').title()}")
    if "NEW_RELATIONSHIP" in conflicts:
        reasoning.append("Previously unseen communication relationships were detected")
    if "TRAFFIC_SPIKE" in conflicts:
        reasoning.append("Traffic volume deviates significantly from the historical pattern")
    if ml_result["available"]:
        reasoning.append(f"ML confidence is {ml_result['confidence_level']} at {ml_result['top_probability']:.0%} for {ml_result['top_class']}")
    if sequence["sequence_detected"]:
        reasoning.append(f"Sequence evidence contributed event order {sequence['event_order']}")
    return {
        "forecast_available": bool(flows),
        "forecast_source": ml_result["forecast_source"],
        "ml_model_loaded": ml_result["available"],
        "predicted_attack_type": predicted_class if predicted_class != "NORMAL" else "NO_CLEAR_ATTACK_PROGRESSION",
        "attack_probability": probability,
        "confidence": round(min(99.0, 35.0 + sequence["sequence_confidence"] * 35.0 + significant * 5.0 + (20.0 if ml_result["available"] else 0.0)), 2),
        "potential_targets": targets,
        "risk_level": _risk_level(len(conflicts), probability),
        "reasoning": reasoning,
        "ml_probabilities": probabilities,
        "ml_confidence_level": ml_result["confidence_level"],
        "ml_top_class": ml_result["top_class"],
        "ml_top_probability": ml_result["top_probability"],
        "hybrid_weights": effective_weights,
        "sequence_analysis": sequence,
        "attack_path": attack_path,
        "attack_stage_probabilities": attack_stages,
        "attack_stage_evidence": attack_stage_evidence,
        "multi_window_analysis": multi_window,
        "relationship_analysis_available": relationship_score is not None,
        "integrity_analysis_available": integrity_score is not None,
        "evidence": {
            "ml": {"available": ml_result["available"], "prediction": ml_result["top_class"], "probability": ml_result["top_probability"], "confidence": ml_result["confidence_level"]},
            "sequence": {"detected": sequence["sequence_detected"], "pattern": sequence["sequence_type"], "event_order": sequence["event_order"]},
            "relationship": {"available": relationship_score is not None, "score": relationship_score},
            "integrity": {"available": integrity_score is not None, "score": integrity_score},
            "threat_intelligence": {"available": threat_match, "matched": threat_match},
        },
        "contributing_signals": [{"source": source, "contribution": round(value, 4), "attribution": "EFFECTIVE_COMPONENT_WEIGHT"} for source, value in contribution_sources.items() if value > 0],
    }
