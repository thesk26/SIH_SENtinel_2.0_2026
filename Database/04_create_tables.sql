-- 04_create_tables.sql
-- Core SENTINEL relational schema.

SET search_path TO sentinel, public;

CREATE TABLE sentinel.devices (
    device_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_name VARCHAR(128) NOT NULL,
    device_type VARCHAR(64) NOT NULL,
    hostname VARCHAR(128),
    ip_address INET,
    mac_address MACADDR,
    operating_system VARCHAR(128),
    zone VARCHAR(128),
    status device_status NOT NULL DEFAULT 'UNKNOWN',
    risk_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (risk_score >= 0 AND risk_score <= 100),
    first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    device_fingerprint_hash VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_device_name_not_blank CHECK (length(trim(device_name)) > 0),
    CONSTRAINT chk_device_device_fingerprint_hash CHECK (device_fingerprint_hash IS NULL OR length(trim(device_fingerprint_hash)) > 0),
    CONSTRAINT uq_devices_identity UNIQUE (device_name, hostname, ip_address, mac_address),
    CONSTRAINT uq_devices_fingerprint UNIQUE (device_fingerprint_hash)
);

CREATE TABLE sentinel.security_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_event_id VARCHAR(255),
    event_fingerprint VARCHAR(128) NOT NULL,
    source_device_id UUID NOT NULL,
    destination_device_id UUID,
    source_ip INET,
    destination_ip INET,
    source_port INTEGER CHECK (source_port BETWEEN 0 AND 65535),
    destination_port INTEGER CHECK (destination_port BETWEEN 0 AND 65535),
    protocol VARCHAR(32),
    event_type VARCHAR(64) NOT NULL,
    event_category VARCHAR(64) NOT NULL,
    severity threat_severity NOT NULL DEFAULT 'MEDIUM',
    raw_event_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    event_timestamp TIMESTAMPTZ NOT NULL,
    ingestion_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_event_identity CHECK (source_event_id IS NOT NULL OR event_fingerprint IS NOT NULL),
    CONSTRAINT uq_security_events_source UNIQUE (source_event_id, source_device_id),
    CONSTRAINT uq_security_events_fingerprint UNIQUE (event_fingerprint, source_device_id, destination_device_id, event_timestamp)
);

CREATE TABLE sentinel.behavioral_baselines (
    baseline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id UUID NOT NULL,
    baseline_type VARCHAR(64) NOT NULL,
    baseline_key VARCHAR(128) NOT NULL,
    observed_value JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurrence_count INTEGER NOT NULL DEFAULT 1 CHECK (occurrence_count >= 0),
    confidence_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (confidence_score >= 0 AND confidence_score <= 100),
    first_observed TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_observed TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    baseline_status baseline_status NOT NULL DEFAULT 'OBSERVED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_behavioral_baselines UNIQUE (device_id, baseline_type, baseline_key)
);

CREATE TABLE sentinel.relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_device_id UUID NOT NULL,
    destination_device_id UUID NOT NULL,
    relationship_type VARCHAR(64) NOT NULL,
    protocol VARCHAR(32),
    port INTEGER CHECK (port BETWEEN 0 AND 65535),
    first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    occurrence_count INTEGER NOT NULL DEFAULT 1 CHECK (occurrence_count >= 0),
    trust_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (trust_score >= 0 AND trust_score <= 100),
    relationship_status relationship_status NOT NULL DEFAULT 'NEW',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_relationships_unique UNIQUE (source_device_id, destination_device_id, relationship_type, protocol, port)
);

CREATE TABLE sentinel.assumptions (
    assumption_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assumption_name VARCHAR(128) NOT NULL,
    assumption_type VARCHAR(64) NOT NULL,
    subject_entity VARCHAR(128) NOT NULL,
    expected_behavior TEXT NOT NULL,
    confidence_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (confidence_score >= 0 AND confidence_score <= 100),
    integrity_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (integrity_score >= 0 AND integrity_score <= 100),
    current_state assumption_state NOT NULL DEFAULT 'OBSERVED',
    supporting_evidence_count INTEGER NOT NULL DEFAULT 0 CHECK (supporting_evidence_count >= 0),
    contradictory_evidence_count INTEGER NOT NULL DEFAULT 0 CHECK (contradictory_evidence_count >= 0),
    first_observed TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_verified TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_assumption_state_trust CHECK ((current_state <> 'TRUSTED') OR (supporting_evidence_count >= 3 AND confidence_score >= 80)),
    CONSTRAINT uq_assumptions_name_subject UNIQUE (assumption_name, subject_entity)
);

CREATE TABLE sentinel.assumption_transitions (
    transition_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assumption_id UUID NOT NULL,
    previous_state assumption_state,
    new_state assumption_state NOT NULL,
    transition_reason VARCHAR(255),
    triggered_by VARCHAR(128),
    confidence_before NUMERIC(5,2) CHECK (confidence_before >= 0 AND confidence_before <= 100),
    confidence_after NUMERIC(5,2) CHECK (confidence_after >= 0 AND confidence_after <= 100),
    transition_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.assumption_evidence (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assumption_id UUID NOT NULL,
    event_id UUID,
    evidence_type VARCHAR(64) NOT NULL,
    evidence_direction evidence_direction NOT NULL,
    evidence_strength NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (evidence_strength >= 0 AND evidence_strength <= 100),
    description TEXT,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.threat_indicators (
    indicator_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    indicator_type VARCHAR(64) NOT NULL,
    indicator_value VARCHAR(255) NOT NULL,
    threat_category VARCHAR(64),
    severity threat_severity NOT NULL DEFAULT 'MEDIUM',
    confidence_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (confidence_score >= 0 AND confidence_score <= 100),
    source VARCHAR(128) NOT NULL,
    description TEXT,
    first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_threat_indicator UNIQUE (indicator_type, indicator_value, source)
);

CREATE TABLE sentinel.attack_paths (
    attack_path_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID,
    path_confidence NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (path_confidence >= 0 AND path_confidence <= 100),
    path_risk NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (path_risk >= 0 AND path_risk <= 100),
    candidate_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (candidate_score >= 0 AND candidate_score <= 100),
    detection_status path_detection_status NOT NULL DEFAULT 'CANDIDATE',
    selected_path_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.attack_path_edges (
    edge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attack_path_id UUID NOT NULL,
    source_device_id UUID NOT NULL,
    destination_device_id UUID NOT NULL,
    sequence_number INTEGER NOT NULL CHECK (sequence_number >= 1),
    temporal_consistency_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (temporal_consistency_score >= 0 AND temporal_consistency_score <= 100),
    relationship_novelty_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (relationship_novelty_score >= 0 AND relationship_novelty_score <= 100),
    assumption_violation_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (assumption_violation_score >= 0 AND assumption_violation_score <= 100),
    abnormal_frequency_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (abnormal_frequency_score >= 0 AND abnormal_frequency_score <= 100),
    threat_intelligence_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (threat_intelligence_score >= 0 AND threat_intelligence_score <= 100),
    attack_stage_alignment_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (attack_stage_alignment_score >= 0 AND attack_stage_alignment_score <= 100),
    edge_risk NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (edge_risk >= 0 AND edge_risk <= 100),
    evidence_summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.incidents (
    incident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_code VARCHAR(64) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity incident_severity NOT NULL DEFAULT 'HIGH',
    status incident_status NOT NULL DEFAULT 'DETECTED',
    affected_device_id UUID,
    attack_path_id UUID,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.incident_timeline (
    timeline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID NOT NULL,
    event_id UUID,
    timeline_event_type VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.response_actions (
    response_action_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID NOT NULL,
    action_type response_action_type NOT NULL,
    action_status response_action_status NOT NULL DEFAULT 'PENDING',
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    executed_at TIMESTAMPTZ,
    executed_by VARCHAR(128),
    action_result TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.security_analysis_results (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    related_event_id UUID,
    related_device_id UUID,
    analysis_type VARCHAR(64) NOT NULL,
    risk_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (risk_score >= 0 AND risk_score <= 100),
    confidence_score NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (confidence_score >= 0 AND confidence_score <= 100),
    decision analysis_decision NOT NULL,
    explanation TEXT,
    evidence_summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sentinel.system_activity (
    activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_type VARCHAR(64) NOT NULL,
    severity activity_severity NOT NULL DEFAULT 'INFO',
    message TEXT NOT NULL,
    related_entity_type VARCHAR(64),
    related_entity_id VARCHAR(128),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
