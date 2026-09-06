import hashlib

from app.schemas.security import SecurityAnalyzeRequest
from app.services.integrity_engine import calculate_integrity


def request(**overrides: object) -> SecurityAnalyzeRequest:
    values = {
        "typing_speed": 60,
        "key_press_mean_ms": 120,
        "mouse_speed": 100,
        "click_frequency": 2,
        "login_hour": 10,
        "device_fingerprint": "device-a",
        "region": "Maharashtra",
        "network_identifier": "network-a",
        "ip_reputation_score": 100,
    }
    values.update(overrides)
    return SecurityAnalyzeRequest(**values)


def test_consistent_profile_has_high_integrity() -> None:
    baseline = {
        "typing_speed": 60,
        "key_press_mean_ms": 120,
        "mouse_speed": 100,
        "click_frequency": 2,
        "login_hour": 10,
        "known_devices": [hashlib.sha256(b"device-a").hexdigest()],
        "known_regions": ["Maharashtra"],
        "known_networks": [hashlib.sha256(b"network-a").hexdigest()],
    }
    result = calculate_integrity(request(), baseline)
    assert result.score >= 80
    assert result.conflicts == []


def test_multiple_conflicts_reduce_integrity() -> None:
    result = calculate_integrity(
        request(device_fingerprint="new", region="Berlin", login_hour=2, typing_speed=300, ip_reputation_score=20, is_vpn_or_proxy=True),
        {},
    )
    assert result.score < 80
    assert "MULTI_SIGNAL_CONFLICT" in result.conflicts
