from app.services.decision_engine import Decision, decide


def test_threshold_decisions() -> None:
    assert decide(90, []).decision == Decision.PASS
    assert decide(65, ["NEW_DEVICE"]).decision == Decision.CHALLENGE
    assert decide(30, []).decision == Decision.BLOCK


def test_critical_conflict_overrides_score() -> None:
    assert decide(95, ["SUSPICIOUS_NETWORK"]).decision == Decision.BLOCK
