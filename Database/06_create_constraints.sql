-- 06_create_constraints.sql
-- Foreign key constraints and validation checks.

SET search_path TO sentinel, public;

ALTER TABLE sentinel.security_events
    ADD CONSTRAINT fk_security_events_source_device
    FOREIGN KEY (source_device_id) REFERENCES sentinel.devices(device_id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_security_events_destination_device
    FOREIGN KEY (destination_device_id) REFERENCES sentinel.devices(device_id) ON DELETE SET NULL;

ALTER TABLE sentinel.behavioral_baselines
    ADD CONSTRAINT fk_behavioral_baselines_device
    FOREIGN KEY (device_id) REFERENCES sentinel.devices(device_id) ON DELETE CASCADE;

ALTER TABLE sentinel.relationships
    ADD CONSTRAINT fk_relationships_source_device
    FOREIGN KEY (source_device_id) REFERENCES sentinel.devices(device_id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_relationships_destination_device
    FOREIGN KEY (destination_device_id) REFERENCES sentinel.devices(device_id) ON DELETE CASCADE;

ALTER TABLE sentinel.assumption_transitions
    ADD CONSTRAINT fk_assumption_transitions_assumption
    FOREIGN KEY (assumption_id) REFERENCES sentinel.assumptions(assumption_id) ON DELETE CASCADE;

ALTER TABLE sentinel.assumption_evidence
    ADD CONSTRAINT fk_assumption_evidence_assumption
    FOREIGN KEY (assumption_id) REFERENCES sentinel.assumptions(assumption_id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_assumption_evidence_event
    FOREIGN KEY (event_id) REFERENCES sentinel.security_events(event_id) ON DELETE SET NULL;

ALTER TABLE sentinel.attack_paths
    ADD CONSTRAINT fk_attack_paths_incident
    FOREIGN KEY (incident_id) REFERENCES sentinel.incidents(incident_id) ON DELETE SET NULL;

ALTER TABLE sentinel.attack_path_edges
    ADD CONSTRAINT fk_attack_path_edges_path
    FOREIGN KEY (attack_path_id) REFERENCES sentinel.attack_paths(attack_path_id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_attack_path_edges_source_device
    FOREIGN KEY (source_device_id) REFERENCES sentinel.devices(device_id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_attack_path_edges_destination_device
    FOREIGN KEY (destination_device_id) REFERENCES sentinel.devices(device_id) ON DELETE RESTRICT;

ALTER TABLE sentinel.incidents
    ADD CONSTRAINT fk_incidents_affected_device
    FOREIGN KEY (affected_device_id) REFERENCES sentinel.devices(device_id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_incidents_attack_path
    FOREIGN KEY (attack_path_id) REFERENCES sentinel.attack_paths(attack_path_id) ON DELETE SET NULL;

ALTER TABLE sentinel.incident_timeline
    ADD CONSTRAINT fk_incident_timeline_incident
    FOREIGN KEY (incident_id) REFERENCES sentinel.incidents(incident_id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_incident_timeline_event
    FOREIGN KEY (event_id) REFERENCES sentinel.security_events(event_id) ON DELETE SET NULL;

ALTER TABLE sentinel.response_actions
    ADD CONSTRAINT fk_response_actions_incident
    FOREIGN KEY (incident_id) REFERENCES sentinel.incidents(incident_id) ON DELETE CASCADE;

ALTER TABLE sentinel.security_analysis_results
    ADD CONSTRAINT fk_security_analysis_results_event
    FOREIGN KEY (related_event_id) REFERENCES sentinel.security_events(event_id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_security_analysis_results_device
    FOREIGN KEY (related_device_id) REFERENCES sentinel.devices(device_id) ON DELETE SET NULL;

-- Additional data integrity checks.
ALTER TABLE sentinel.devices
    ADD CONSTRAINT chk_devices_risk CHECK (risk_score >= 0 AND risk_score <= 100),
    ADD CONSTRAINT chk_devices_first_seen CHECK (first_seen <= last_seen);

ALTER TABLE sentinel.behavioral_baselines
    ADD CONSTRAINT chk_baselines_dates CHECK (first_observed <= last_observed),
    ADD CONSTRAINT chk_baselines_confidence CHECK (confidence_score >= 0 AND confidence_score <= 100);

ALTER TABLE sentinel.relationships
    ADD CONSTRAINT chk_relationships_dates CHECK (first_seen <= last_seen),
    ADD CONSTRAINT chk_relationships_trust CHECK (trust_score >= 0 AND trust_score <= 100);

ALTER TABLE sentinel.assumptions
    ADD CONSTRAINT chk_assumptions_dates CHECK (first_observed <= COALESCE(last_verified, first_observed)),
    ADD CONSTRAINT chk_assumptions_support CHECK (supporting_evidence_count >= 0 AND contradictory_evidence_count >= 0),
    ADD CONSTRAINT chk_assumptions_confidence CHECK (confidence_score >= 0 AND confidence_score <= 100),
    ADD CONSTRAINT chk_assumptions_integrity CHECK (integrity_score >= 0 AND integrity_score <= 100);

ALTER TABLE sentinel.incidents
    ADD CONSTRAINT chk_incidents_times CHECK (detected_at <= COALESCE(resolved_at, detected_at));

ALTER TABLE sentinel.attack_path_edges
    ADD CONSTRAINT chk_attack_path_edges_order UNIQUE (attack_path_id, sequence_number);
