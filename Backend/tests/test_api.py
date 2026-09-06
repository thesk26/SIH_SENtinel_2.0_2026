from uuid import uuid4

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_collect_and_analyze() -> None:
    suffix = uuid4().hex[:10]
    username = f"test_user_{suffix}"
    register = client.post("/api/auth/register", json={"username": username, "email": f"{suffix}@example.com", "password": "strong-password"})
    assert register.status_code == 201
    login = client.post("/api/auth/login", json={"username": username, "password": "strong-password"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    collected = client.post("/api/behavior/collect", headers=headers, json={"typing_speed": 60, "login_hour": 10, "device_fingerprint": "device-a", "region": "Maharashtra", "network_identifier": "network-a"})
    assert collected.status_code == 200
    analyzed = client.post("/api/security/analyze", headers=headers, json={"typing_speed": 60, "login_hour": 10, "device_fingerprint": "device-a", "region": "Maharashtra", "network_identifier": "network-a"})
    assert analyzed.status_code == 200
    assert analyzed.json()["decision"] in {"PASS", "CHALLENGE", "BLOCK"}
    events = client.get("/api/security/events", headers=headers)
    assert events.status_code == 200
    assert len(events.json()) == 1


def test_network_analysis_quarantines_suspicious_flow() -> None:
    suffix = uuid4().hex[:10]
    username = f"network_user_{suffix}"
    register = client.post("/api/auth/register", json={"username": username, "email": f"{suffix}@example.com", "password": "strong-password"})
    assert register.status_code == 201
    login = client.post("/api/auth/login", json={"username": username, "password": "strong-password"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    normal = client.post("/api/network/analyze", headers=headers, json={"source_ip": "10.0.0.1", "destination_ip": "10.0.0.2", "packet_count": 10, "byte_count": 1000, "request_frequency": 1})
    assert normal.status_code == 200
    assert normal.json()["baseline_eligible"] is True
    suspicious = client.post("/api/network/analyze", headers=headers, json={"source_ip": "10.0.0.1", "destination_ip": "10.0.0.99", "destination_port": 5432, "packet_count": 1000, "byte_count": 10000000, "request_frequency": 50})
    assert suspicious.status_code == 200
    assert suspicious.json()["baseline_eligible"] is False
    assert suspicious.json()["forecast"]["forecast_source"] == "RULE_BASED_FALLBACK"


def test_demo_mode_is_labeled_and_validates_scenarios() -> None:
    demo = client.post("/api/network/demo", json={"scenario": "suspicious"})
    assert demo.status_code == 200
    assert demo.json()["label"] == "SIMULATED DEMO DATA"
    assert demo.json()["flows"]
    invalid = client.post("/api/network/demo", json={"scenario": "production"})
    assert invalid.status_code == 422


def test_empty_forecast_response_is_explicit() -> None:
    suffix = uuid4().hex[:10]
    username = f"empty_forecast_{suffix}"
    client.post("/api/auth/register", json={"username": username, "email": f"{suffix}@example.com", "password": "strong-password"})
    login = client.post("/api/auth/login", json={"username": username, "password": "strong-password"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    response = client.post("/api/security/forecast", headers=headers)
    assert response.status_code == 200
    assert response.json()["forecast_available"] is False
    assert response.json()["predicted_attack_type"] == "NO_DATA"
    assert response.json()["attack_probability"] is None


def test_dashboard_and_system_health_routes_are_available() -> None:
    assert client.get("/system/health").status_code == 200
    assert client.get("/api/dashboard/summary").status_code == 401
