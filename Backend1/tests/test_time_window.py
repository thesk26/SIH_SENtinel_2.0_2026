from datetime import datetime, timedelta
from types import SimpleNamespace

from app.services.hybrid_weight_service import adaptive_weights
from app.services.time_window_analyzer import aggregate_window, select_window


def make_flow(timestamp: datetime, flow_id: str, bytes_sent: int = 100) -> SimpleNamespace:
    return SimpleNamespace(
        id=flow_id,
        source_entity="source",
        destination_entity=f"destination-{flow_id}",
        destination_port=443,
        protocol="TCP",
        packet_count=10,
        byte_count=bytes_sent,
        flow_duration_ms=100,
        timestamp=timestamp,
        connection_status="success",
        derived_features={},
    )


def test_five_minute_window_includes_boundary_and_excludes_old_flow() -> None:
    reference = datetime(2026, 1, 1, 12, 0, 0)
    boundary = make_flow(reference - timedelta(minutes=5), "boundary")
    old = make_flow(reference - timedelta(minutes=5, seconds=1), "old")
    selected = select_window([old, boundary], 5, reference)
    assert [flow.id for flow in selected] == ["boundary"]


def test_window_deduplicates_same_flow() -> None:
    reference = datetime(2026, 1, 1, 12, 0, 0)
    current = make_flow(reference, "same")
    aggregate = aggregate_window([current, current], 15, reference)
    assert aggregate["flow_count"] == 1
    assert aggregate["connections_per_minute"] == 1 / 15


def test_adaptive_weights_are_normalized_when_ml_is_unavailable() -> None:
    weights = adaptive_weights(ml_available=False, ml_confidence_level="LOW", sequence_available=True, relationship_available=True, integrity_available=True)
    assert weights["ml"] == 0
    assert sum(weights.values()) == 1
    assert weights["sequence"] > 0.25


def test_low_confidence_ml_is_downweighted() -> None:
    high = adaptive_weights(ml_available=True, ml_confidence_level="HIGH", sequence_available=True, relationship_available=True, integrity_available=True)
    low = adaptive_weights(ml_available=True, ml_confidence_level="LOW", sequence_available=True, relationship_available=True, integrity_available=True)
    assert sum(high.values()) == 1
    assert sum(low.values()) == 1
    assert low["ml"] < high["ml"]
