-- 05_create_indexes.sql
-- Indexes designed for SENTINEL runtime access patterns.

SET search_path TO sentinel, public;

CREATE INDEX idx_devices_name ON sentinel.devices (device_name);
CREATE INDEX idx_devices_type ON sentinel.devices (device_type);
CREATE INDEX idx_devices_status ON sentinel.devices (status);
CREATE INDEX idx_devices_zone ON sentinel.devices (zone);
CREATE INDEX idx_devices_ip ON sentinel.devices (ip_address);
CREATE INDEX idx_devices_mac ON sentinel.devices (mac_address);
CREATE INDEX idx_devices_last_seen ON sentinel.devices (last_seen DESC);

CREATE INDEX idx_events_timestamp ON sentinel.security_events (event_timestamp DESC);
CREATE INDEX idx_events_source_event_id ON sentinel.security_events (source_event_id);
CREATE INDEX idx_events_fingerprint ON sentinel.security_events (event_fingerprint);
CREATE INDEX idx_events_source_ip ON sentinel.security_events (source_ip);
CREATE INDEX idx_events_destination_ip ON sentinel.security_events (destination_ip);
CREATE INDEX idx_events_type ON sentinel.security_events (event_type);
CREATE INDEX idx_events_source_device ON sentinel.security_events (source_device_id);
CREATE INDEX idx_events_destination_device ON sentinel.security_events (destination_device_id);
CREATE INDEX idx_events_severity ON sentinel.security_events (severity);

CREATE INDEX idx_baselines_device ON sentinel.behavioral_baselines (device_id);
CREATE INDEX idx_baselines_type_key ON sentinel.behavioral_baselines (baseline_type, baseline_key);
CREATE INDEX idx_baselines_status ON sentinel.behavioral_baselines (baseline_status);
CREATE INDEX idx_baselines_last_observed ON sentinel.behavioral_baselines (last_observed DESC);

CREATE INDEX idx_relationships_source ON sentinel.relationships (source_device_id);
CREATE INDEX idx_relationships_destination ON sentinel.relationships (destination_device_id);
CREATE INDEX idx_relationships_status ON sentinel.relationships (relationship_status);
CREATE INDEX idx_relationships_type ON sentinel.relationships (relationship_type);
CREATE INDEX idx_relationships_last_seen ON sentinel.relationships (last_seen DESC);
CREATE INDEX idx_relationships_trust ON sentinel.relationships (trust_score);

CREATE INDEX idx_assumptions_state ON sentinel.assumptions (current_state);
CREATE INDEX idx_assumptions_type ON sentinel.assumptions (assumption_type);
CREATE INDEX idx_assumptions_confidence ON sentinel.assumptions (confidence_score DESC);
CREATE INDEX idx_assumptions_last_verified ON sentinel.assumptions (last_verified DESC);

CREATE INDEX idx_assumption_transitions_assumption ON sentinel.assumption_transitions (assumption_id);
CREATE INDEX idx_assumption_transitions_state ON sentinel.assumption_transitions (new_state);
CREATE INDEX idx_assumption_transitions_time ON sentinel.assumption_transitions (transition_timestamp DESC);

CREATE INDEX idx_assumption_evidence_assumption ON sentinel.assumption_evidence (assumption_id);
CREATE INDEX idx_assumption_evidence_event ON sentinel.assumption_evidence (event_id);
CREATE INDEX idx_assumption_evidence_direction ON sentinel.assumption_evidence (evidence_direction);
CREATE INDEX idx_assumption_evidence_observed_at ON sentinel.assumption_evidence (observed_at DESC);

CREATE INDEX idx_threat_indicators_type_value ON sentinel.threat_indicators (indicator_type, indicator_value);
CREATE INDEX idx_threat_indicators_severity ON sentinel.threat_indicators (severity);
CREATE INDEX idx_threat_indicators_last_seen ON sentinel.threat_indicators (last_seen DESC);
CREATE INDEX idx_threat_indicators_category ON sentinel.threat_indicators (threat_category);

CREATE INDEX idx_attack_paths_incident ON sentinel.attack_paths (incident_id);
CREATE INDEX idx_attack_paths_confidence ON sentinel.attack_paths (path_confidence DESC);
CREATE INDEX idx_attack_paths_risk ON sentinel.attack_paths (path_risk DESC);
CREATE INDEX idx_attack_paths_status ON sentinel.attack_paths (detection_status);

CREATE INDEX idx_attack_path_edges_path ON sentinel.attack_path_edges (attack_path_id);
CREATE INDEX idx_attack_path_edges_sequence ON sentinel.attack_path_edges (attack_path_id, sequence_number);
CREATE INDEX idx_attack_path_edges_source ON sentinel.attack_path_edges (source_device_id);
CREATE INDEX idx_attack_path_edges_destination ON sentinel.attack_path_edges (destination_device_id);
CREATE INDEX idx_attack_path_edges_risk ON sentinel.attack_path_edges (edge_risk DESC);

CREATE INDEX idx_incidents_status ON sentinel.incidents (status);
CREATE INDEX idx_incidents_severity ON sentinel.incidents (severity);
CREATE INDEX idx_incidents_device ON sentinel.incidents (affected_device_id);
CREATE INDEX idx_incidents_attack_path ON sentinel.incidents (attack_path_id);
CREATE INDEX idx_incidents_detected_at ON sentinel.incidents (detected_at DESC);

CREATE INDEX idx_incident_timeline_incident ON sentinel.incident_timeline (incident_id);
CREATE INDEX idx_incident_timeline_event ON sentinel.incident_timeline (event_id);
CREATE INDEX idx_incident_timeline_timestamp ON sentinel.incident_timeline (timestamp DESC);

CREATE INDEX idx_response_actions_incident ON sentinel.response_actions (incident_id);
CREATE INDEX idx_response_actions_status ON sentinel.response_actions (action_status);
CREATE INDEX idx_response_actions_requested_at ON sentinel.response_actions (requested_at DESC);

CREATE INDEX idx_analysis_event ON sentinel.security_analysis_results (related_event_id);
CREATE INDEX idx_analysis_device ON sentinel.security_analysis_results (related_device_id);
CREATE INDEX idx_analysis_decision ON sentinel.security_analysis_results (decision);
CREATE INDEX idx_analysis_risk ON sentinel.security_analysis_results (risk_score DESC);

CREATE INDEX idx_system_activity_type ON sentinel.system_activity (activity_type);
CREATE INDEX idx_system_activity_severity ON sentinel.system_activity (severity);
CREATE INDEX idx_system_activity_created_at ON sentinel.system_activity (created_at DESC);
