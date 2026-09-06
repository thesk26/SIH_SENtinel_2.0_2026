-- 07_seed_demo_data.sql
-- Demo seed dataset for SENTINEL front-end and dashboard workflows.

SET search_path TO sentinel, public;

INSERT INTO sentinel.devices (
    device_id, device_name, device_type, hostname, ip_address, mac_address,
    operating_system, zone, status, risk_score, first_seen, last_seen,
    device_fingerprint_hash
) VALUES
    ('11111111-1111-4111-8111-111111111111', 'CAM-07', 'camera', 'cam-07-sec', '10.10.5.17', '00:1B:44:11:22:33', 'Linux', 'PERIMETER', 'AT_RISK', 82.10, '2026-09-01 08:10:00+00', '2026-09-06 08:40:00+00', 'hash-cam-07'),
    ('22222222-2222-4222-8222-222222222222', 'CORE-SW-01', 'switch', 'core-sw-01', '10.10.0.11', '00:1A:2B:3C:4D:5E', 'Cisco IOS', 'CORE', 'ONLINE', 12.00, '2026-08-17 00:00:00+00', '2026-09-06 08:40:00+00', 'hash-core-sw-01'),
    ('33333333-3333-4333-8333-333333333333', 'SRV-APP-02', 'server', 'srv-app-02', '10.10.3.21', '00:AA:BB:CC:DD:EE', 'Ubuntu 22.04', 'APP', 'ONLINE', 68.20, '2026-08-18 01:00:00+00', '2026-09-06 08:35:00+00', 'hash-srv-app-02'),
    ('44444444-4444-4444-8444-444444444444', 'DB-PRIMARY', 'database', 'db-primary', '10.10.4.5', '00:11:22:33:44:55', 'Ubuntu 22.04', 'DATABASE', 'ONLINE', 26.00, '2026-08-20 02:00:00+00', '2026-09-06 08:30:00+00', 'hash-db-primary'),
    ('55555555-5555-4555-8555-555555555555', 'WS-ENG-09', 'workstation', 'ws-eng-09', '10.10.1.19', '00:12:34:56:78:9A', 'Windows 11', 'USER', 'ONLINE', 18.00, '2026-08-19 04:00:00+00', '2026-09-06 08:40:00+00', 'hash-ws-eng-09'),
    ('66666666-6666-4666-8666-666666666666', 'LAP-SEC-05', 'laptop', 'lap-sec-05', '10.10.1.27', '00:0F:AA:BB:CC:DD', 'Windows 11', 'USER', 'OFFLINE', 13.00, '2026-08-25 00:00:00+00', '2026-09-05 19:00:00+00', 'hash-lap-sec-05'),
    ('77777777-7777-4777-8777-777777777777', 'WS-GRAPH-02', 'workstation', 'ws-graph-02', '10.10.1.44', '00:DE:AD:BE:EF:00', 'Windows 11', 'USER', 'ONLINE', 23.00, '2026-08-30 06:00:00+00', '2026-09-06 08:38:00+00', 'hash-ws-graph-02'),
    ('88888888-8888-4888-8888-888888888888', 'FW-EDGE-01', 'firewall', 'fw-edge-01', '10.10.9.1', '00:FF:EE:DD:CC:BB', 'FortiOS', 'EDGE', 'ONLINE', 30.00, '2026-08-21 09:00:00+00', '2026-09-06 08:40:00+00', 'hash-fw-edge-01'),
    ('99999999-9999-4999-8999-999999999999', 'VPN-GW-01', 'gateway', 'vpn-gw-01', '10.10.8.25', '00:81:02:03:04:05', 'Linux', 'EDGE', 'ONLINE', 41.00, '2026-08-29 02:30:00+00', '2026-09-06 08:39:00+00', 'hash-vpn-gw-01'),
    ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa', 'SRV-LOG-01', 'server', 'srv-log-01', '10.10.3.10', '00:AA:00:11:22:33', 'Ubuntu 22.04', 'APP', 'ONLINE', 16.00, '2026-08-19 10:00:00+00', '2026-09-06 08:37:00+00', 'hash-srv-log-01');

INSERT INTO sentinel.security_events (
    event_id, source_event_id, event_fingerprint, source_device_id, destination_device_id,
    source_ip, destination_ip, source_port, destination_port, protocol, event_type,
    event_category, severity, raw_event_metadata, event_timestamp, ingestion_timestamp
) VALUES
    ('11111111-0001-4000-8000-000000000001', 'evt-1001', 'fp-1001', '11111111-1111-4111-8111-111111111111', '33333333-3333-4333-8333-333333333333', '10.10.5.17', '10.10.3.21', 5000, 8080, 'TCP', 'UNUSUAL_OUTBOUND_CONNECTION', 'NETWORK', 'HIGH', '{"flow_id": "flow-1001", "bytes": 4210, "flags": ["SYN"]}', '2026-09-06 08:14:00+00', '2026-09-06 08:15:00+00'),
    ('11111111-0001-4000-8000-000000000002', 'evt-1002', 'fp-1002', '33333333-3333-4333-8333-333333333333', '44444444-4444-4444-8444-444444444444', '10.10.3.21', '10.10.4.5', 5432, 5432, 'TCP', 'DATABASE_ACCESS', 'DATABASE', 'MEDIUM', '{"query": "SELECT * FROM admin_users"}', '2026-09-06 08:16:00+00', '2026-09-06 08:17:00+00'),
    ('11111111-0001-4000-8000-000000000003', 'evt-1003', 'fp-1003', '11111111-1111-4111-8111-111111111111', '44444444-4444-4444-8444-444444444444', '10.10.5.17', '10.10.4.5', 4555, 5432, 'TCP', 'RECONNAISSANCE', 'NETWORK', 'HIGH', '{"bytes": 1550, "service": "postgres"}', '2026-09-06 08:19:00+00', '2026-09-06 08:20:00+00'),
    ('11111111-0001-4000-8000-000000000004', 'evt-1004', 'fp-1004', '33333333-3333-4333-8333-333333333333', '44444444-4444-4444-8444-444444444444', '10.10.3.21', '10.10.4.5', 6000, 22, 'TCP', 'SUSPICIOUS_SSH_ACCESS', 'ACCESS', 'CRITICAL', '{"user": "root", "source": "app server"}', '2026-09-06 08:22:00+00', '2026-09-06 08:23:00+00'),
    ('11111111-0001-4000-8000-000000000005', 'evt-1005', 'fp-1005', '99999999-9999-4999-8999-999999999999', '44444444-4444-4444-8444-444444444444', '10.10.8.25', '10.10.4.5', 443, 443, 'TCP', 'VPN_LOGIN', 'ACCESS', 'LOW', '{"vpn_name": "CorpVPN"}', '2026-09-06 08:12:00+00', '2026-09-06 08:18:00+00'),
    ('11111111-0001-4000-8000-000000000006', 'evt-1006', 'fp-1006', '22222222-2222-4222-8222-222222222222', '33333333-3333-4333-8333-333333333333', '10.10.0.11', '10.10.3.21', 443, 443, 'TCP', 'NORMAL_SERVICE_TRAFIC', 'NETWORK', 'LOW', '{"channel": "internal"}', '2026-09-06 08:10:00+00', '2026-09-06 08:12:00+00');

INSERT INTO sentinel.behavioral_baselines (
    baseline_id, device_id, baseline_type, baseline_key, observed_value, occurrence_count,
    confidence_score, first_observed, last_observed, baseline_status
) VALUES
    ('21111111-1111-4111-8111-111111111111', '22222222-2222-4222-8222-222222222222', 'KNOWN_DESTINATION', '10.10.3.21', '{"destination": "10.10.3.21"}', 24, 96.00, '2026-08-20 00:00:00+00', '2026-09-06 08:10:00+00', 'OBSERVED'),
    ('21111111-1111-4111-8111-111111111112', '22222222-2222-4222-8222-222222222222', 'KNOWN_PORT', '443', '{"port": 443}', 18, 90.00, '2026-08-20 00:00:00+00', '2026-09-06 08:10:00+00', 'OBSERVED'),
    ('21111111-1111-4111-8111-111111111113', '11111111-1111-4111-8111-111111111111', 'KNOWN_DESTINATION', '10.10.3.21', '{"destination": "10.10.3.21"}', 3, 42.00, '2026-09-01 08:00:00+00', '2026-09-06 08:14:00+00', 'UNIQUE_IN_WINDOW'),
    ('21111111-1111-4111-8111-111111111114', '11111111-1111-4111-8111-111111111111', 'KNOWN_PORT', '8080', '{"port": 8080}', 2, 38.00, '2026-09-01 08:00:00+00', '2026-09-06 08:14:00+00', 'NEW_VS_HISTORICAL');

INSERT INTO sentinel.relationships (
    relationship_id, source_device_id, destination_device_id, relationship_type,
    protocol, port, first_seen, last_seen, occurrence_count, trust_score, relationship_status
) VALUES
    ('31111111-1111-4111-8111-111111111111', '22222222-2222-4222-8222-222222222222', '33333333-3333-4333-8333-333333333333', 'SERVICE', 'TCP', 443, '2026-08-20 00:00:00+00', '2026-09-06 08:10:00+00', 62, 92.00, 'TRUSTED'),
    ('31111111-1111-4111-8111-111111111112', '33333333-3333-4333-8333-333333333333', '44444444-4444-4444-8444-444444444444', 'DATABASE', 'TCP', 5432, '2026-08-21 00:00:00+00', '2026-09-06 08:16:00+00', 33, 82.00, 'TRUSTED'),
    ('31111111-1111-4111-8111-111111111113', '11111111-1111-4111-8111-111111111111', '33333333-3333-4333-8333-333333333333', 'UNUSUAL', 'TCP', 8080, '2026-09-06 08:14:00+00', '2026-09-06 08:14:00+00', 1, 28.00, 'SUSPICIOUS'),
    ('31111111-1111-4111-8111-111111111114', '11111111-1111-4111-8111-111111111111', '44444444-4444-4444-8444-444444444444', 'RECONNAISSANCE', 'TCP', 5432, '2026-09-06 08:19:00+00', '2026-09-06 08:19:00+00', 1, 33.00, 'SUSPICIOUS');

INSERT INTO sentinel.assumptions (
    assumption_id, assumption_name, assumption_type, subject_entity, expected_behavior,
    confidence_score, integrity_score, current_state, supporting_evidence_count,
    contradictory_evidence_count, first_observed, last_verified
) VALUES
    ('41111111-1111-4111-8111-111111111111', 'Core service path', 'COMMUNICATION', 'SRV-APP-02', 'App server communicates only with database and logging services', 88.00, 76.00, 'TRUSTED', 7, 1, '2026-08-20 00:00:00+00', '2026-09-06 08:15:00+00'),
    ('41111111-1111-4111-8111-111111111112', 'Camera traffic integrity', 'DEVICE_BEHAVIOR', 'CAM-07', 'Camera should not access database service directly', 92.00, 60.00, 'WEAKENED', 3, 2, '2026-09-01 08:00:00+00', '2026-09-06 08:20:00+00'),
    ('41111111-1111-4111-8111-111111111113', 'Internal app trust', 'ACCESS_PATTERN', 'SRV-APP-02', 'Application should not initiate SSH to database server', 79.00, 58.00, 'LEARNING', 2, 1, '2026-09-06 08:00:00+00', '2026-09-06 08:22:00+00'),
    ('41111111-1111-4111-8111-111111111114', 'Firewall baseline', 'NETWORK_CONTROL', 'FW-EDGE-01', 'Firewall should allow only known egress ports', 65.00, 84.00, 'CANDIDATE', 1, 0, '2026-09-06 08:01:00+00', '2026-09-06 08:01:00+00');

INSERT INTO sentinel.assumption_transitions (
    transition_id, assumption_id, previous_state, new_state, transition_reason,
    triggered_by, confidence_before, confidence_after, transition_timestamp
) VALUES
    ('51111111-1111-4111-8111-111111111111', '41111111-1111-4111-8111-111111111112', 'OBSERVED', 'WEAKENED', 'Unexpected database access from camera device', 'external_event', 76.00, 92.00, '2026-09-06 08:20:00+00'),
    ('51111111-1111-4111-8111-111111111112', '41111111-1111-4111-8111-111111111111', 'LEARNING', 'TRUSTED', 'Repeated successful service communication across 7 days', 'behavioral_baseline', 77.00, 88.00, '2026-09-06 08:10:00+00');

INSERT INTO sentinel.assumption_evidence (
    evidence_id, assumption_id, event_id, evidence_type, evidence_direction,
    evidence_strength, description, observed_at, metadata
) VALUES
    ('61111111-1111-4111-8111-111111111111', '41111111-1111-4111-8111-111111111112', '11111111-0001-4000-8000-000000000001', 'NETWORK_CONNECTION', 'CONTRADICTORY', 87.00, 'Camera initiated direct communication to app server on unauthorized port 8080', '2026-09-06 08:14:00+00', '{"port": 8080, "source": "CAM-07"}'),
    ('61111111-1111-4111-8111-111111111112', '41111111-1111-4111-8111-111111111111', '11111111-0001-4000-8000-000000000006', 'NETWORK_CONNECTION', 'SUPPORTING', 76.00, 'Internal service communication matched historical baseline', '2026-09-06 08:10:00+00', '{"service": "core to app"}'),
    ('61111111-1111-4111-8111-111111111113', '41111111-1111-4111-8111-111111111113', '11111111-0001-4000-8000-000000000004', 'ACCESS', 'CONTRADICTORY', 91.00, 'Database was reached via SSH from app service using elevated privileges', '2026-09-06 08:22:00+00', '{"user": "root"}');

INSERT INTO sentinel.threat_indicators (
    indicator_id, indicator_type, indicator_value, threat_category, severity,
    confidence_score, source, description, first_seen, last_seen
) VALUES
    ('71111111-1111-4111-8111-111111111111', 'IP', '10.10.5.17', 'MALICIOUS_ENDPOINT', 'HIGH', 88.00, 'Threat feed', 'Camera source device showing anomalous lateral movement behavior', '2026-09-01 00:00:00+00', '2026-09-06 08:22:00+00'),
    ('71111111-1111-4111-8111-111111111112', 'FILE_HASH', 'a1b2c3d4e5f6', 'MALWARE', 'CRITICAL', 96.00, 'EDR', 'Malware hash linked to credential harvesting pattern', '2026-09-06 08:18:00+00', '2026-09-06 08:22:00+00'),
    ('71111111-1111-4111-8111-111111111113', 'DOMAIN', 'cdn-update.internal', 'PHISHING', 'MEDIUM', 58.00, 'Custom intel', 'Suspicious domain resolved during reconnaissance activity', '2026-09-06 08:13:00+00', '2026-09-06 08:19:00+00');

INSERT INTO sentinel.attack_paths (
    attack_path_id, incident_id, path_confidence, path_risk, candidate_score,
    detection_status, selected_path_reason
) VALUES
    ('81111111-1111-4111-8111-111111111111', NULL, 82.00, 91.00, 79.00, 'DETECTED', 'Lateral movement from camera to app server to database with anomaly escalation'),
    ('81111111-1111-4111-8111-111111111112', NULL, 61.00, 66.00, 58.00, 'CANDIDATE', 'Possible privilege abuse via VPN access');

INSERT INTO sentinel.attack_path_edges (
    edge_id, attack_path_id, source_device_id, destination_device_id, sequence_number,
    temporal_consistency_score, relationship_novelty_score, assumption_violation_score,
    abnormal_frequency_score, threat_intelligence_score, attack_stage_alignment_score,
    edge_risk, evidence_summary
) VALUES
    ('91111111-1111-4111-8111-111111111111', '81111111-1111-4111-8111-111111111111', '11111111-1111-4111-8111-111111111111', '33333333-3333-4333-8333-333333333333', 1, 78.00, 92.00, 88.00, 84.00, 79.00, 91.00, 90.00, 'Direct lateral movement from camera to application server using nonstandard 8080 port'),
    ('91111111-1111-4111-8111-111111111112', '81111111-1111-4111-8111-111111111111', '33333333-3333-4333-8333-333333333333', '44444444-4444-4444-8444-444444444444', 2, 81.00, 73.00, 92.00, 88.00, 83.00, 89.00, 94.00, 'App server queried database after abnormal access and privilege escalation attempt'),
    ('91111111-1111-4111-8111-111111111113', '81111111-1111-4111-8111-111111111112', '99999999-9999-4999-8999-999999999999', '44444444-4444-4444-8444-444444444444', 1, 74.00, 61.00, 40.00, 55.00, 62.00, 67.00, 58.00, 'VPN gateway to database path is suspicious but not yet confirmed');

INSERT INTO sentinel.incidents (
    incident_id, incident_code, title, description, severity, status,
    affected_device_id, attack_path_id, detected_at, resolved_at
) VALUES
    ('a1111111-1111-4111-8111-111111111111', 'INC-2026-0147', 'Database lateral movement', 'Potential lateral movement from camera device to application and database systems.', 'HIGH', 'INVESTIGATING', '11111111-1111-4111-8111-111111111111', '81111111-1111-4111-8111-111111111111', '2026-09-06 08:25:00+00', NULL);

INSERT INTO sentinel.incident_timeline (
    timeline_id, incident_id, event_id, timeline_event_type, description, timestamp, metadata
) VALUES
    ('b1111111-1111-4111-8111-111111111111', 'a1111111-1111-4111-8111-111111111111', '11111111-0001-4000-8000-000000000001', 'EVENT_DETECTED', 'Abnormal camera-to-app communication detected', '2026-09-06 08:14:00+00', '{"severity": "HIGH"}'),
    ('b1111111-1111-4111-8111-111111111112', 'a1111111-1111-4111-8111-111111111111', '11111111-0001-4000-8000-000000000003', 'EVENT_DETECTED', 'Reconnaissance to database server observed', '2026-09-06 08:19:00+00', '{"severity": "HIGH"}'),
    ('b1111111-1111-4111-8111-111111111113', 'a1111111-1111-4111-8111-111111111111', NULL, 'INCIDENT_CREATED', 'Incident assigned for investigation', '2026-09-06 08:25:00+00', '{"source": "sentinel"}');

INSERT INTO sentinel.response_actions (
    response_action_id, incident_id, action_type, action_status, requested_at,
    executed_at, executed_by, action_result, notes
) VALUES
    ('c1111111-1111-4111-8111-111111111111', 'a1111111-1111-4111-8111-111111111111', 'VERIFY', 'COMPLETED', '2026-09-06 08:26:00+00', '2026-09-06 08:27:00+00', 'soc-analyst-01', 'Confirmed unusual communication path', 'Validated camera traffic against baseline and block recommendation'),
    ('c1111111-1111-4111-8111-111111111112', 'a1111111-1111-4111-8111-111111111111', 'ISOLATE', 'PENDING', '2026-09-06 08:27:00+00', NULL, 'soc-operator-02', NULL, 'Awaiting approval for network isolation of camera and app server');

INSERT INTO sentinel.security_analysis_results (
    analysis_id, related_event_id, related_device_id, analysis_type, risk_score,
    confidence_score, decision, explanation, evidence_summary
) VALUES
    ('d1111111-1111-4111-8111-111111111111', '11111111-0001-4000-8000-000000000001', '11111111-1111-4111-8111-111111111111', 'NETWORK_RISK', 88.00, 90.00, 'INVESTIGATE', 'Unexpected outbound service to app server is inconsistent with camera baseline', 'Direct communication plus suspicious port 8080'),
    ('d1111111-1111-4111-8111-111111111112', '11111111-0001-4000-8000-000000000004', '33333333-3333-4333-8333-333333333333', 'ACCESS_RISK', 94.00, 92.00, 'BLOCK', 'Application server attempted SSH to database with elevated privileges', 'SSH credential misuse and abnormal database access');

INSERT INTO sentinel.system_activity (
    activity_id, activity_type, severity, message, related_entity_type, related_entity_id, metadata
) VALUES
    ('e1111111-1111-4111-8111-111111111111', 'SECURITY_EVENT', 'HIGH', 'Unusual camera communication chain created alert', 'device', '11111111-1111-4111-8111-111111111111', '{"event_id": "11111111-0001-4000-8000-000000000001"}'),
    ('e1111111-1111-4111-8111-111111111112', 'ASSUMPTION_STATUS', 'MEDIUM', 'Camera communication assumption weakened', 'assumption', '41111111-1111-4111-8111-111111111112', '{"state": "WEAKENED"}'),
    ('e1111111-1111-4111-8111-111111111113', 'ATTACK_PATH', 'CRITICAL', 'Attack path candidate detected for lateral movement', 'attack_path', '81111111-1111-4111-8111-111111111111', '{"risk": 91.00}');
