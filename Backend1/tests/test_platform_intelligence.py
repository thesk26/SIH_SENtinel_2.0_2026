from datetime import datetime, timedelta
from types import SimpleNamespace

from app.services.attack_path_service import predict_attack_path
from app.services.attack_stage_service import stage_evidence, stage_probabilities
from app.services.event_ingestion_service import event_fingerprint
from app.services.relationship_delta_service import relationship_deltas
from app.services.time_window_analyzer import aggregate_window
from app.schemas.network_traffic import NetworkTrafficCreate


def flow(destination: str, port: int, minutes: int = 0) -> SimpleNamespace:
    return SimpleNamespace(
        source_entity="workstation",
        destination_entity=destination,
        destination_port=port,
        protocol="TCP",
        packet_count=10,
        byte_count=100,
        flow_duration_ms=100,
        timestamp=datetime(2026, 1, 1, 12, 0) + timedelta(minutes=minutes),
        connection_status="success",
        derived_features={"conflicts": ["NEW_RELATIONSHIP"] if destination == "database" else [], "rapid_connections": destination == "server"},
    )


def test_relationship_deltas_identify_new_entities_ports_and_protocols() -> None:
    baseline = [flow("server", 443)]
    current = [flow("server", 443), flow("database", 5432)]
    deltas = relationship_deltas(current, baseline)
    assert deltas["new_destinations"] == ["database"]
    assert deltas["new_ports"] == [5432]
    assert deltas["new_relationships"]


def test_attack_path_and_stage_probabilities_are_evidence_based() -> None:
    flows = [flow("server", 443), flow("database", 5432, 1)]
    sequence = {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.82}
    targets = [{"entity": "database", "target_risk_score": 88, "reason": ["New relationship"]}]
    path = predict_attack_path(flows, targets, sequence)
    stages = stage_probabilities(sequence, "LATERAL_MOVEMENT", 0.72)
    assert path["attack_path_detected"] is True
    assert path["predicted_path"][-1] == "database"
    assert stages["LATERAL_MOVEMENT"] == 0.82


def test_window_distinguishes_unique_values_from_baseline_novelty() -> None:
    baseline = [flow("server", 443)]
    current = [flow("server", 443), flow("database", 5432)]
    aggregate = aggregate_window(current, 15, baseline_flows=baseline)
    assert aggregate["unique_destinations_in_window"] == 2
    assert aggregate["new_destinations_against_baseline"] == ["database"]
    assert aggregate["new_destination_count"] == 1
    assert aggregate["new_ports_against_baseline"] == [5432]


def test_missing_timestamp_fingerprint_is_deterministic() -> None:
    payload = NetworkTrafficCreate(source_ip="10.0.0.1", destination_ip="10.0.0.2", packet_count=1, byte_count=2)
    first_fingerprint = event_fingerprint(payload, "source", "destination")
    second_fingerprint = event_fingerprint(payload, "source", "destination")
    assert first_fingerprint == second_fingerprint


def test_disconnected_path_is_not_claimed_with_high_confidence() -> None:
    disconnected = [flow("server-a", 443), flow("server-b", 5432, 1)]
    disconnected[1].source_entity = "unrelated-source"
    sequence = {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.8}
    target = [{"entity": "server-b", "target_risk_score": 90, "reason": ["critical"]}]
    path = predict_attack_path(disconnected, target, sequence)
    assert path["attack_path_detected"] is False
    assert path["attack_path_confidence"] == 0.0


def test_unrelated_suspicious_flow_does_not_change_path_risk() -> None:
    first = flow("server", 443)
    first.source_entity = "a"
    first.id = "AB"
    second = flow("database", 5432, 1)
    second.source_entity = "server"
    second.id = "BC"
    second.derived_features = {"conflicts": ["NEW_RELATIONSHIP"]}
    unrelated = flow("other", 443, 2)
    unrelated.source_entity = "x"
    unrelated.id = "XY"
    unrelated.derived_features = {"conflicts": ["NEW_RELATIONSHIP"]}
    sequence = {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.8}
    target = [{"entity": "database", "target_risk_score": 80}]
    without_unrelated = predict_attack_path([first, second], target, sequence)
    with_unrelated = predict_attack_path([first, second, unrelated], target, sequence)
    assert with_unrelated["attack_path_risk"] == without_unrelated["attack_path_risk"]
    assert with_unrelated["global_environmental_context"]["unrelated_suspicious_events"] == 1


def test_historically_trusted_connected_path_is_not_meaningful() -> None:
    first = flow("server", 443)
    first.source_entity = "employee"
    second = flow("database", 5432, 1)
    second.source_entity = "server"
    baseline = [first, second]
    path = predict_attack_path([first, second], [], {"sequence_detected": False}, baseline_flows=baseline)
    assert path["attack_path_detected"] is False
    assert path["attack_path_confidence"] < 0.5


def test_suspicious_new_progression_has_stronger_edge_evidence() -> None:
    first = flow("server", 443)
    first.source_entity = "workstation"
    first.derived_features = {"conflicts": ["ASSUMPTION_VIOLATION"]}
    second = flow("database", 5432, 1)
    second.source_entity = "server"
    second.derived_features = {"conflicts": ["NEW_RELATIONSHIP", "ASSUMPTION_VIOLATION"]}
    sequence = {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.9}
    path = predict_attack_path([first, second], [{"entity": "database", "target_risk_score": 88}], sequence)
    assert path["attack_path_confidence"] > 0.5
    assert path["path_edges"][1]["signals"]["assumption_violation"]["detected"] is True


def test_reverse_temporal_order_reduces_path_confidence() -> None:
    ordered_first = flow("server", 443)
    ordered_first.source_entity = "workstation"
    ordered_second = flow("database", 5432, 1)
    ordered_second.source_entity = "server"
    reverse_first = flow("server", 443, 1)
    reverse_first.source_entity = "workstation"
    reverse_second = flow("database", 5432)
    reverse_second.source_entity = "server"
    sequence = {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.8}
    target = [{"entity": "database", "target_risk_score": 80}]
    ordered = predict_attack_path([ordered_first, ordered_second], target, sequence)
    reversed_path = predict_attack_path([reverse_first, reverse_second], target, sequence)
    assert reversed_path["attack_path_confidence"] < ordered["attack_path_confidence"]
    assert reversed_path["path_edges"][1]["signals"]["temporal_consistency"]["score"] == 0.0


def test_critical_target_can_raise_risk_without_confidence() -> None:
    critical = flow("critical-database", 5432)
    critical.source_entity = "workstation"
    path = predict_attack_path([critical], [{"entity": "critical-database", "target_risk_score": 95}], {"sequence_detected": False})
    assert path["attack_path_confidence"] == 0.0
    assert path["attack_path_risk"] > 0.3


def test_threat_intelligence_is_an_edge_signal_not_confirmation() -> None:
    first = flow("server", 443)
    first.source_entity = "workstation"
    first.derived_features = {"threat_intelligence": {"matched": True, "confidence": 0.8}}
    second = flow("database", 5432, 1)
    second.source_entity = "server"
    second.derived_features = {}
    sequence = {"sequence_detected": False, "sequence_type": "NO_CLEAR_ATTACK_PROGRESSION"}
    path = predict_attack_path([first, second], [{"entity": "database", "target_risk_score": 60}], sequence, baseline_flows=[first, second])
    assert path["path_edges"][0]["signals"]["threat_intelligence"] == {"detected": True, "score": 0.8}
    assert path["attack_path_detected"] is False


def _path_flow(source: str, destination: str, minutes: int, conflicts: list[str] | None = None) -> SimpleNamespace:
    current = flow(destination, 443, minutes)
    current.source_entity = source
    current.derived_features = {"conflicts": conflicts or []}
    return current


def test_shorter_candidate_with_stronger_evidence_is_selected() -> None:
    flows = [
        _path_flow("a", "b", 0, ["NEW_RELATIONSHIP", "ASSUMPTION_VIOLATION"]),
        _path_flow("b", "target", 1, ["NEW_RELATIONSHIP", "ASSUMPTION_VIOLATION"]),
        _path_flow("a", "x", 0),
        _path_flow("x", "y", 1),
        _path_flow("y", "z", 2),
        _path_flow("z", "target", 3),
    ]
    baseline = [_path_flow("a", "x", 0), _path_flow("x", "y", 1), _path_flow("y", "z", 2), _path_flow("z", "target", 3)]
    path = predict_attack_path(flows, [{"entity": "target", "target_risk_score": 80}], {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.9}, baseline_flows=baseline)
    assert path["predicted_path"] == ["a", "b", "target"]
    assert "Path-specific assumption violation evidence" in path["selected_path_reason"]


def test_longer_candidate_with_stronger_evidence_is_selected() -> None:
    flows = [
        _path_flow("a", "b", 0),
        _path_flow("b", "target", 1),
        _path_flow("a", "x", 0, ["NEW_RELATIONSHIP", "ASSUMPTION_VIOLATION"]),
        _path_flow("x", "y", 1, ["NEW_RELATIONSHIP", "ASSUMPTION_VIOLATION"]),
        _path_flow("y", "target", 2, ["NEW_RELATIONSHIP", "ASSUMPTION_VIOLATION"]),
    ]
    baseline = [_path_flow("a", "b", 0), _path_flow("b", "target", 1)]
    path = predict_attack_path(flows, [{"entity": "target", "target_risk_score": 80}], {"sequence_detected": True, "sequence_type": "POSSIBLE_LATERAL_MOVEMENT", "sequence_confidence": 0.9}, baseline_flows=baseline)
    assert path["predicted_path"] == ["a", "x", "y", "target"]
    assert path["selected_path_score"] > 0.0


def test_long_historically_trusted_candidate_stays_low_confidence() -> None:
    flows = [_path_flow("a", "b", 0), _path_flow("b", "c", 1), _path_flow("c", "d", 2), _path_flow("d", "target", 3)]
    path = predict_attack_path(flows, [{"entity": "target", "target_risk_score": 90}], {"sequence_detected": False}, baseline_flows=list(flows))
    assert path["attack_path_detected"] is False
    assert path["attack_path_confidence"] < 0.5


def test_unsupported_stages_report_insufficient_evidence() -> None:
    evidence = stage_evidence({}, None, 0.0)
    assert evidence["EXECUTION"]["status"] == "INSUFFICIENT_EVIDENCE"
    assert evidence["PERSISTENCE"]["status"] == "INSUFFICIENT_EVIDENCE"
    assert evidence["PRIVILEGE_ESCALATION"]["status"] == "INSUFFICIENT_EVIDENCE"
