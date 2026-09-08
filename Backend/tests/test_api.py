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


def test_authorized_device_controls_collector_telemetry() -> None:
    suffix = uuid4().hex[:10]
    register = client.post("/api/auth/register", json={"username": f"collector_{suffix}", "email": f"{suffix}@example.com", "password": "strong-password"})
    assert register.status_code == 201
    login = client.post("/api/auth/login", json={"username": f"collector_{suffix}", "password": "strong-password"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    device = client.post("/api/devices", headers=headers, json={"hostname": "localhost-agent", "ip_address": "127.0.0.1", "operating_system": "Windows", "device_type": "workstation", "consent_reference": "local-owner-approval"})
    assert device.status_code == 201
    device_id = device.json()["id"]
    flow = {"device_id": device_id, "source_event_id": f"collector-{suffix}", "ingestion_source": "LOCAL_COLLECTOR", "source_ip": "127.0.0.1", "destination_ip": "127.0.0.1", "destination_port": 8000, "packet_count": 1, "byte_count": 128, "flow_duration_ms": 2}

    denied = client.post("/api/network/traffic", headers=headers, json=flow)
    assert denied.status_code == 403
    authorized = client.post(f"/api/devices/{device_id}/authorize", headers=headers, json={"consent_reference": "local-owner-approval", "monitoring_scope": {"hosts": ["127.0.0.1"], "purpose": "local integration test"}})
    assert authorized.status_code == 200
    activated = client.post(f"/api/devices/{device_id}/activate", headers=headers)
    assert activated.status_code == 200
    collected = client.post("/api/network/traffic", headers=headers, json=flow)
    assert collected.status_code == 200
    listed = client.get("/api/devices", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["authorization_state"] == "ACTIVE"
    assert listed.json()[0]["status"] == "ONLINE"
    revoked = client.post(f"/api/devices/{device_id}/revoke", headers=headers)
    assert revoked.status_code == 200
    denied_after_revoke = client.post("/api/network/traffic", headers=headers, json={**flow, "source_event_id": f"revoked-{suffix}"})
    assert denied_after_revoke.status_code == 403


def test_response_actions_are_simulated_and_evidence_is_hashed() -> None:
    suffix = uuid4().hex[:10]
    client.post("/api/auth/register", json={"username": f"response_{suffix}", "email": f"response-{suffix}@example.com", "password": "strong-password"})
    login = client.post("/api/auth/login", json={"username": f"response_{suffix}", "password": "strong-password"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    action = client.post("/api/response/actions", headers=headers, json={"action": "MONITOR", "reason": "Verify local test signal"})
    assert action.status_code == 200
    assert action.json()["mode"] == "SIMULATION"
    evidence = client.post("/api/response/evidence", headers=headers, json={"event_id": "test-event", "evidence": {"risk_score": 91, "source": "LOCAL_COLLECTOR"}})
    assert evidence.status_code == 200
    assert len(evidence.json()["evidence_hash"]) == 64


def test_collector_heartbeat_telemetry_and_stale_status() -> None:
    suffix = uuid4().hex[:10]
    client.post("/api/auth/register", json={"username": f"telemetry_{suffix}", "email": f"telemetry-{suffix}@example.com", "password": "strong-password"})
    login = client.post("/api/auth/login", json={"username": f"telemetry_{suffix}", "password": "strong-password"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    device = client.post("/api/devices", headers=headers, json={"hostname": "telemetry-host", "operating_system": "Windows", "device_type": "workstation"}).json()
    device_id = device["id"]
    client.post(f"/api/devices/{device_id}/authorize", headers=headers, json={"monitoring_scope": {"hosts": ["localhost"]}})
    assert client.post(f"/api/devices/{device_id}/activate", headers=headers).status_code == 200
    heartbeat = client.post("/api/collector/heartbeat", headers=headers, json={"device_id": device_id, "status": "online"})
    assert heartbeat.status_code == 200
    telemetry = client.post("/api/collector/telemetry", headers=headers, json={"device_id": device_id, "cpu_percent": 42.5, "memory_percent": 38.0, "disk_percent": 51.0, "uptime_seconds": 120, "os_information": {"system": "Windows"}, "interfaces": {"Ethernet": "up"}, "bytes_sent": 1000, "bytes_received": 2000, "connection_count": 2})
    assert telemetry.status_code == 200
    assert telemetry.json()["data_source"] == "REAL"
    diagnostics = client.get("/api/collector/diagnostics", headers=headers)
    assert diagnostics.status_code == 200
    assert diagnostics.json()["telemetry_received"] == 1
    stale = client.post("/api/collector/heartbeat", headers=headers, json={"device_id": device_id, "timestamp": "2020-01-01T00:00:00Z"})
    assert stale.status_code == 200
    status = client.get("/api/collector/status", headers=headers)
    assert status.status_code == 200
    assert status.json()["devices"][0]["status"] == "OFFLINE"
