from __future__ import annotations

from collections import defaultdict

def _edge_key(flow) -> tuple[str, str]:
    return flow.source_entity, flow.destination_entity

def _edge_flows(flows: list, source: str, destination: str) -> list:
    return [flow for flow in flows if _edge_key(flow) == (source, destination)]

def _score_frequency(current_flows: list, baseline_flows: list) -> tuple[bool, float]:
    current_count = len(current_flows)
    baseline_count = len(baseline_flows)
    if not baseline_count:
        return False, 0.0
    ratio = current_count / baseline_count
    return ratio >= 1.5, round(min(1.0, max(0.0, (ratio - 1.0) / 2.0)), 3)

def _temporal_score(previous_flows: list, current_flows: list) -> float:
    if not previous_flows or not current_flows:
        return 0.0
    return 1.0 if max(flow.timestamp for flow in previous_flows) <= min(flow.timestamp for flow in current_flows) else 0.0

def _edge_intelligence(source: str, destination: str, current_flows: list, baseline_flows: list, previous_flows: list, sequence: dict) -> dict:
    current_features = [flow.derived_features or {} for flow in current_flows]
    baseline_edge_flows = _edge_flows(baseline_flows, source, destination)
    conflicts = {conflict for features in current_features for conflict in features.get("conflicts", [])}
    novelty_detected = bool(current_flows) and not baseline_edge_flows
    assumption_detected = "ASSUMPTION_VIOLATION" in conflicts
    temporal_score = _temporal_score(previous_flows, current_flows) if previous_flows else 1.0
    frequency_detected, frequency_score = _score_frequency(current_flows, baseline_edge_flows)
    threat_matches = [features.get("threat_intelligence", {}) for features in current_features]
    threat_detected = any(bool(match.get("matched")) for match in threat_matches)
    threat_score = max((float(match.get("confidence", 0.0)) for match in threat_matches if match.get("matched")), default=0.0)
    stage_supported = sequence.get("sequence_detected") and sequence.get("sequence_type") != "NO_CLEAR_ATTACK_PROGRESSION"
    stage = sequence.get("sequence_type", "").replace("POSSIBLE_", "") if stage_supported else None
    stage_score = float(sequence.get("sequence_confidence", 0.0)) if stage_supported else 0.0
    edge_risk = min(1.0, (1.0 if novelty_detected else 0.0) * 0.3 + (1.0 if assumption_detected else 0.0) * 0.25 + frequency_score * 0.15 + threat_score * 0.15 + stage_score * 0.15)
    evidence_summary: list[str] = []
    if novelty_detected:
        evidence_summary.append("Relationship absent from historical baseline")
    if assumption_detected:
        evidence_summary.append("Trusted assumption contradicted")
    if frequency_detected:
        evidence_summary.append("Connection frequency exceeds historical baseline")
    if threat_detected:
        evidence_summary.append("Threat-intelligence indicator matched")
    if stage_supported:
        evidence_summary.append(f"Aligned with {stage.replace('_', ' ').title()} stage evidence")
    return {
        "source": source,
        "destination": destination,
        "supporting_flow_ids": [getattr(flow, "id", None) for flow in current_flows],
        "signals": {
            "relationship_novelty": {"detected": novelty_detected, "score": round(1.0 if novelty_detected else 0.0, 3)},
            "assumption_violation": {"detected": assumption_detected, "score": round(1.0 if assumption_detected else 0.0, 3)},
            "temporal_consistency": {"score": round(temporal_score, 3)},
            "abnormal_frequency": {"detected": frequency_detected, "score": frequency_score},
            "threat_intelligence": {"detected": threat_detected, "score": round(threat_score, 3)},
            "attack_stage_alignment": {"stage": stage, "score": round(stage_score, 3)},
        },
        "edge_risk": round(edge_risk, 3),
        "evidence_summary": evidence_summary,
    }


def _candidate_intelligence(path: list[str], ordered: list, baseline: list, sequence: dict, target_risk: float) -> tuple[list[dict], float, list[str]]:
    edges: list[dict] = []
    for index, (source, destination) in enumerate(zip(path, path[1:])):
        current_flows = _edge_flows(ordered, source, destination)
        previous_flows = _edge_flows(ordered, path[index - 1], source) if index else []
        edges.append(_edge_intelligence(source, destination, current_flows, baseline, previous_flows, sequence))
    if not edges:
        return [], 0.0, []
    temporal = sum(edge["signals"]["temporal_consistency"]["score"] for edge in edges) / len(edges)
    edge_evidence = sum(
        sum(edge["signals"][signal]["score"] for signal in ("relationship_novelty", "assumption_violation", "abnormal_frequency", "threat_intelligence", "attack_stage_alignment")) / 5
        for edge in edges
    ) / len(edges)
    stage_alignment = sum(edge["signals"]["attack_stage_alignment"]["score"] for edge in edges) / len(edges)
    candidate_score = min(1.0, 0.2 + temporal * 0.25 + edge_evidence * 0.25 + stage_alignment * 0.15 + target_risk * 0.1 + min(1.0, len(edges) / 4) * 0.05)
    reasons: list[str] = []
    if temporal >= 0.75:
        reasons.append("Strong temporal progression")
    if sum(edge["signals"]["assumption_violation"]["detected"] for edge in edges) >= 1:
        reasons.append("Path-specific assumption violation evidence")
    if sum(edge["signals"]["relationship_novelty"]["detected"] for edge in edges) >= 1:
        reasons.append("Path-specific relationship novelty")
    if stage_alignment > 0:
        reasons.append("Consistent with attack-stage evidence")
    return edges, round(candidate_score, 3), reasons

def _candidate_paths(adjacency: dict[str, list[tuple[str, object]]], starts: list[str], target: str | None) -> list[tuple[list[str], list[str]]]:
    queue = [(start, [start], []) for start in starts]
    candidates: list[tuple[list[str], list[str]]] = []
    while queue:
        node, path, evidence = queue.pop(0)
        if node == target:
            candidates.append((path, evidence))
            continue
        for destination, flow in adjacency.get(node, []):
            if destination not in path:
                queue.append((destination, [*path, destination], [*evidence, getattr(flow, "id", None)]))
    return candidates


def _select_candidate(candidates: list[tuple[list[str], list[str]]], ordered: list, baseline: list, sequence: dict, target_risk: float) -> tuple[list[str], list[str], list[dict], float, list[str]]:
    if not candidates:
        return [], [], [], 0.0, []
    ranked_candidates = []
    for path, evidence in candidates:
        candidate_edges, candidate_score, candidate_reasons = _candidate_intelligence(path, ordered, baseline, sequence, target_risk)
        ranked_candidates.append((candidate_score, path, evidence, candidate_edges, candidate_reasons))
    selected_score, nodes, supporting_flows, selected_edges, selected_reasons = max(ranked_candidates, key=lambda candidate: candidate[0])
    return nodes, supporting_flows, selected_edges, selected_score, selected_reasons


def _path_metrics(nodes: list[str], path_edges: list[dict], adjacency: dict[str, list[tuple[str, object]]], target_risk: float, has_target: bool) -> tuple[float, float, bool, list[str]]:
    edge_risks = [edge["edge_risk"] for edge in path_edges]
    supported_edges = sum(bool(edge["evidence_summary"]) for edge in path_edges)
    temporal_consistency = sum(edge["signals"]["temporal_consistency"]["score"] for edge in path_edges) / len(path_edges) if path_edges else 0.0
    stage_alignment = max((edge["signals"]["attack_stage_alignment"]["score"] for edge in path_edges), default=0.0)
    meaningful_progression = len(path_edges) >= 2 or (len(path_edges) == 1 and len(adjacency.get(nodes[0], [])) > 1) if nodes else False
    confidence = min(0.95, 0.04 + len(path_edges) * 0.03 + supported_edges * 0.2 + temporal_consistency * 0.25 + stage_alignment * 0.15) if meaningful_progression else 0.0
    risk = min(0.99, (sum(edge_risks) / len(edge_risks) if edge_risks else 0.0) * 0.6 + target_risk * 0.4)
    non_threat_evidence = sum(bool(edge["evidence_summary"]) and any(signal["detected"] for name, signal in edge["signals"].items() if name != "threat_intelligence" and "detected" in signal) for edge in path_edges)
    detected = meaningful_progression and (stage_alignment > 0 or non_threat_evidence >= 2) and supported_edges > 0 and risk >= 0.35 and confidence >= 0.5
    reasons = ["Target criticality contributes separately from path evidence"] if has_target else []
    if not detected:
        reasons.append("Insufficient connected and suspicious path evidence")
    return round(confidence, 3), round(risk, 3), detected, reasons


def predict_attack_path(flows: list, targets: list[dict], sequence: dict, baseline_flows: list | None = None) -> dict:
    ordered = sorted(flows, key=lambda item: item.timestamp)
    baseline = list(baseline_flows or [])
    adjacency: dict[str, list[tuple[str, object]]] = defaultdict(list)
    for flow in ordered:
        adjacency.setdefault(flow.source_entity, []).append((flow.destination_entity, flow))
    high_value = targets[0]["entity"] if targets else None
    high_value = high_value or (ordered[-1].destination_entity if ordered else None)
    target_risk = min(1.0, targets[0]["target_risk_score"] / 100) if targets else 0.0
    sources = list(dict.fromkeys(flow.source_entity for flow in ordered))
    destinations = {flow.destination_entity for flow in ordered}
    starts = [source for source in sources if source not in destinations] or sources
    candidates = _candidate_paths(adjacency, starts, high_value)
    nodes, supporting_flows, path_edges, selected_candidate_score, selected_path_reason = _select_candidate(candidates, ordered, baseline, sequence, target_risk)
    reasons = list(selected_path_reason)
    reasons.extend(edge_reason for edge in path_edges for edge_reason in edge["evidence_summary"])
    confidence, risk, detected, metric_reasons = _path_metrics(nodes, path_edges, adjacency, target_risk, bool(targets))
    reasons.extend(metric_reasons)
    unrelated_suspicious = sum(bool((flow.derived_features or {}).get("conflicts")) for flow in ordered if getattr(flow, "id", None) not in supporting_flows)
    return {
        "attack_path_detected": detected,
        "attack_path_confidence": round(confidence, 3),
        "attack_path_risk": round(risk, 3),
        "path_risk_score": round(risk, 3),
        "predicted_path": nodes,
        "supporting_flow_ids": supporting_flows,
        "path_edges": path_edges,
        "selected_path_score": selected_candidate_score,
        "selected_path_reason": list(dict.fromkeys(selected_path_reason)),
        "global_environmental_context": {"overall_network_risk": round(min(0.99, sum(bool((flow.derived_features or {}).get("conflicts")) for flow in ordered) / max(1, len(ordered))), 3), "unrelated_suspicious_events": unrelated_suspicious},
        "reasoning": list(dict.fromkeys(reasons)),
    }
