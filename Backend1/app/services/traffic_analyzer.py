from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.network_traffic import NetworkTraffic
from app.graph.assumption_graph import AssumptionGraph, AssumptionNode
from app.graph.relationship_engine import relationship_graph_score
from app.services.network_baseline_service import build_baseline, relationship_evidence
from app.services.network_feature_extractor import extract_features
from app.services.relationship_delta_service import relationship_deltas
from app.utils.helpers import hash_identifier, utc_now


def _entity(value: str) -> str:
    return hash_identifier(value) or "unknown"


def record_flow(db: Session, user_id: str, payload) -> tuple[NetworkTraffic, dict, dict, list[str]]:
    source = _entity(payload.source_ip)
    destination = _entity(payload.destination_ip)
    recent = list(db.scalars(select(NetworkTraffic).where(NetworkTraffic.user_id == user_id, NetworkTraffic.baseline_eligible.is_(True)).order_by(NetworkTraffic.timestamp.desc()).limit(200)))
    flow = NetworkTraffic(user_id=user_id, source_entity=source, destination_entity=destination, source_port=payload.source_port, destination_port=payload.destination_port, protocol=payload.protocol.upper(), packet_count=payload.packet_count, byte_count=payload.byte_count, flow_duration_ms=payload.flow_duration_ms, timestamp=payload.timestamp or utc_now(), tcp_flags=payload.tcp_flags, connection_status=payload.connection_status.lower(), request_frequency=payload.request_frequency)
    features = extract_features(flow, recent)
    baseline = build_baseline(recent, source)
    relationship_score, conflicts = relationship_evidence(flow, baseline)
    graph = AssumptionGraph(user_id)
    for relationship in baseline["common_relationships"]:
        graph.add(AssumptionNode(kind="COMMUNICATES_WITH", reference=f"{relationship['destination']}:{relationship['protocol']}:{relationship['port']}", confidence=min(1.0, relationship["frequency"] / max(1, baseline["sample_count"])), frequency=relationship["frequency"], consistency=baseline["confidence"]))
    if baseline["sample_count"]:
        relationship_score = relationship_graph_score(graph, f"{destination}:{flow.protocol}:{flow.destination_port}", conflicts)
    deltas = relationship_deltas([flow], recent)
    if baseline["sample_count"] and deltas["new_relationships"] and "NEW_RELATIONSHIP" not in conflicts:
        conflicts.append("NEW_RELATIONSHIP")
    flow.derived_features = {**features, "conflicts": conflicts, "relationship_score": relationship_score, "relationship_deltas": deltas}
    return flow, {"relationship_score": relationship_score, "baseline": baseline}, features, conflicts


def persist_flow(db: Session, flow: NetworkTraffic, baseline_eligible: bool) -> NetworkTraffic:
    flow.baseline_eligible = baseline_eligible
    db.add(flow)
    db.commit()
    db.refresh(flow)
    return flow


def baseline_update_allowed(integrity_score: float, conflicts: list[str], historical_count: int) -> bool:
    from app.core.config import settings

    critical_conflicts = {"SUSPICIOUS_NETWORK", "MULTI_SIGNAL_CRITICAL", "POSSIBLE_LATERAL_MOVEMENT", "TRAFFIC_SPIKE", "REPEATED_CONNECTION_FAILURES"}
    return integrity_score >= settings.baseline_update_threshold and not critical_conflicts.intersection(conflicts) and (historical_count > 0 or not conflicts)


def user_flows(db: Session, user_id: str, limit: int = 200) -> list[NetworkTraffic]:
    return list(db.scalars(select(NetworkTraffic).where(NetworkTraffic.user_id == user_id, NetworkTraffic.baseline_eligible.is_(True), (NetworkTraffic.is_duplicate.is_(False) | NetworkTraffic.is_duplicate.is_(None))).order_by(NetworkTraffic.timestamp.desc()).limit(limit)))


def all_user_flows(db: Session, user_id: str, limit: int = 200) -> list[NetworkTraffic]:
    return list(db.scalars(select(NetworkTraffic).where(NetworkTraffic.user_id == user_id, (NetworkTraffic.is_duplicate.is_(False) | NetworkTraffic.is_duplicate.is_(None))).order_by(NetworkTraffic.timestamp.desc()).limit(limit)))
