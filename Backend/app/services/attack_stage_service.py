from __future__ import annotations


def stage_probabilities(sequence: dict, ml_class: str | None, ml_probability: float) -> dict[str, float]:
    stages = {"RECONNAISSANCE": 0.0, "INITIAL_ACCESS": 0.0, "EXECUTION": 0.0, "PERSISTENCE": 0.0, "PRIVILEGE_ESCALATION": 0.0, "LATERAL_MOVEMENT": 0.0, "COLLECTION": 0.0, "EXFILTRATION": 0.0}
    sequence_type = sequence.get("sequence_type", "")
    if "RECONNAISSANCE" in sequence_type:
        stages["RECONNAISSANCE"] = sequence.get("sequence_confidence", 0.0)
    if "LATERAL" in sequence_type or ml_class == "LATERAL_MOVEMENT":
        stages["LATERAL_MOVEMENT"] = max(sequence.get("sequence_confidence", 0.0), ml_probability if ml_class == "LATERAL_MOVEMENT" else 0.0)
    if ml_class == "PORT_SCAN":
        stages["RECONNAISSANCE"] = max(stages["RECONNAISSANCE"], ml_probability)
    if ml_class == "DATA_EXFILTRATION":
        stages["EXFILTRATION"] = ml_probability
        stages["COLLECTION"] = min(1.0, ml_probability * 0.8)
    if ml_class == "BRUTE_FORCE":
        stages["INITIAL_ACCESS"] = ml_probability
    return {name: round(value, 4) for name, value in stages.items()}


def stage_evidence(sequence: dict, ml_class: str | None, ml_probability: float) -> dict[str, dict]:
    probabilities = stage_probabilities(sequence, ml_class, ml_probability)
    evidence = {}
    for stage, probability in probabilities.items():
        if probability <= 0:
            evidence[stage] = {"status": "INSUFFICIENT_EVIDENCE", "signals": []}
        else:
            evidence[stage] = {"status": "SUPPORTED", "signals": ["SEQUENCE_ANALYSIS"] if stage in sequence.get("sequence_type", "") else ["ML_MODEL"]}
    return evidence
