-- 03_create_enums.sql
-- PostgreSQL enum types used by SENTINEL.

CREATE TYPE sentinel.device_status AS ENUM ('ONLINE', 'OFFLINE', 'AT_RISK', 'UNKNOWN');
CREATE TYPE sentinel.baseline_status AS ENUM ('UNIQUE_IN_WINDOW', 'NEW_VS_HISTORICAL', 'OBSERVED', 'LEARNING', 'ANOMALOUS', 'EXPIRED');
CREATE TYPE sentinel.relationship_status AS ENUM ('NEW', 'OBSERVED', 'LEARNING', 'TRUSTED', 'WEAKENED', 'SUSPICIOUS');
CREATE TYPE sentinel.assumption_state AS ENUM ('OBSERVED', 'CANDIDATE', 'LEARNING', 'TRUSTED', 'WEAKENED', 'EXPIRED', 'RETIRED');
CREATE TYPE sentinel.evidence_direction AS ENUM ('SUPPORTING', 'CONTRADICTORY', 'NEUTRAL');
CREATE TYPE sentinel.threat_severity AS ENUM ('INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
CREATE TYPE sentinel.incident_severity AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
CREATE TYPE sentinel.incident_status AS ENUM ('DETECTED', 'INVESTIGATING', 'CONTAINED', 'RESOLVED', 'CLOSED');
CREATE TYPE sentinel.response_action_type AS ENUM ('VERIFY', 'INVESTIGATE', 'ISOLATE', 'PRESERVE_EVIDENCE', 'RECOVER');
CREATE TYPE sentinel.response_action_status AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED');
CREATE TYPE sentinel.analysis_decision AS ENUM ('PASS', 'CHALLENGE', 'BLOCK', 'INVESTIGATE');
CREATE TYPE sentinel.activity_severity AS ENUM ('INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
CREATE TYPE sentinel.path_detection_status AS ENUM ('CANDIDATE', 'DETECTED', 'VALIDATED', 'DISCARDED');
