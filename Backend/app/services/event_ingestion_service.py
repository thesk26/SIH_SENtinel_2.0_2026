from __future__ import annotations

import hashlib
import json
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.network_traffic import NetworkTraffic
from app.services.traffic_analyzer import record_flow
from app.services.threat_intelligence import LocalThreatIntelligenceProvider


def event_fingerprint(payload, source: str, destination: str) -> str:
    values = {
        "source": source,
        "destination": destination,
        "source_port": payload.source_port,
        "destination_port": payload.destination_port,
        "protocol": payload.protocol.upper(),
        "packet_count": payload.packet_count,
        "byte_count": payload.byte_count,
        "duration": payload.flow_duration_ms,
        "timestamp": payload.timestamp.isoformat() if payload.timestamp else None,
        "status": payload.connection_status.lower(),
        "frequency": payload.request_frequency,
    }
    return hashlib.sha256(json.dumps(values, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def ingest_flow(db: Session, user_id: str, payload) -> tuple[NetworkTraffic, bool]:
    source = hashlib.sha256(payload.source_ip.encode()).hexdigest()
    destination = hashlib.sha256(payload.destination_ip.encode()).hexdigest()
    fingerprint = event_fingerprint(payload, source, destination)
    duplicate_query = select(NetworkTraffic).where(NetworkTraffic.user_id == user_id, NetworkTraffic.event_fingerprint == fingerprint)
    if payload.source_event_id:
        duplicate_query = select(NetworkTraffic).where(NetworkTraffic.user_id == user_id, NetworkTraffic.source_event_id == payload.source_event_id)
    duplicate = db.scalar(duplicate_query)
    flow, analysis, features, conflicts = record_flow(db, user_id, payload)
    flow.source_event_id = payload.source_event_id
    flow.event_fingerprint = fingerprint
    flow.ingestion_source = payload.ingestion_source.upper()
    flow.is_duplicate = duplicate is not None
    flow.derived_features = {**features, "conflicts": conflicts, "relationship_score": analysis["relationship_score"], "duplicate_event": duplicate is not None}
    intel = LocalThreatIntelligenceProvider().lookup(payload.destination_ip)
    flow.derived_features["threat_intelligence"] = {"matched": intel.matched, "source": intel.source, "confidence": intel.confidence, "observed_at": intel.observed_at.isoformat()}
    if intel.matched and "KNOWN_MALICIOUS_INDICATOR" not in conflicts:
        conflicts.append("KNOWN_MALICIOUS_INDICATOR")
        flow.derived_features["conflicts"] = conflicts
    return flow, duplicate is not None
