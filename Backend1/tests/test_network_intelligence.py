from types import SimpleNamespace
from datetime import datetime, timedelta

from app.services.attack_sequence_analyzer import analyze_sequence
from app.services.forecasting_engine import forecast
from app.services.network_baseline_service import build_baseline, relationship_evidence
from app.services.network_feature_extractor import extract_features
from app.services.target_prediction_service import predict_targets
from app.services.traffic_analyzer import baseline_update_allowed


def flow(destination: str, *, when: datetime, failures: bool = False, spike: int = 100) -> SimpleNamespace:
    return SimpleNamespace(
        source_entity="source-a",
        destination_entity=destination,
        destination_port=443,
        protocol="TCP",
        packet_count=10,
        byte_count=spike,
        timestamp=when,
        connection_status="failed" if failures else "success",
        request_frequency=25,
        derived_features={"rapid_connections": True, "traffic_spike": spike > 500, "repeated_failures": 3 if failures else 0},
    )


def test_feature_extraction_detects_rapid_connections() -> None:
    current = flow("server-a", when=datetime.utcnow())
    features = extract_features(current, [current])
    assert features["rapid_connections"] is True
    assert features["unique_destinations"] == 1


def test_new_relationship_is_lower_confidence() -> None:
    baseline = build_baseline([flow("server-a", when=datetime.utcnow() - timedelta(days=1))], "source-a")
    score, conflicts = relationship_evidence(flow("server-b", when=datetime.utcnow()), baseline)
    assert score < 50
    assert "NEW_RELATIONSHIP" in conflicts


def test_forecast_explains_related_sequence() -> None:
    flows = [flow("server-a", when=datetime.utcnow() - timedelta(minutes=2), failures=True), flow("server-b", when=datetime.utcnow(), spike=1000)]
    result = forecast(flows, ["NEW_RELATIONSHIP"])
    assert result["forecast_available"] is True
    assert result["attack_probability"] > 15
    assert result["reasoning"]
    assert result["potential_targets"]


def test_suspicious_flow_is_not_eligible_for_baseline() -> None:
    assert baseline_update_allowed(92, [], 1) is True
    assert baseline_update_allowed(92, ["TRAFFIC_SPIKE"], 1) is False


def test_lateral_sequence_preserves_event_order() -> None:
    first = flow("server-a", when=datetime.utcnow() - timedelta(minutes=2))
    first.derived_features = {"conflicts": ["NEW_RELATIONSHIP"], "unique_destinations": 2}
    first.destination_port = 22
    second = flow("server-b", when=datetime.utcnow() - timedelta(minutes=1))
    second.derived_features = {"unique_destinations": 2}
    second.destination_port = 22
    third = flow("server-c", when=datetime.utcnow())
    third.derived_features = {"conflicts": ["NEW_RELATIONSHIP"], "unique_destinations": 2}
    third.destination_port = 22
    sequence = analyze_sequence([third, first, second])
    assert sequence["event_order"]
    assert sequence["sequence_type"] == "POSSIBLE_LATERAL_MOVEMENT"
    assert sequence["event_order"] == sorted(sequence["event_order"])


def test_target_prediction_returns_ranked_targets_only() -> None:
    suspicious = flow("critical-server", when=datetime.utcnow(), spike=1000)
    suspicious.destination_port = 5432
    suspicious.derived_features["conflicts"] = ["NEW_RELATIONSHIP"]
    targets = predict_targets([suspicious], ["NEW_RELATIONSHIP"])
    assert len(targets) == 1
    assert targets[0]["target_risk_score"] >= 45
    assert targets[0]["reason"]
