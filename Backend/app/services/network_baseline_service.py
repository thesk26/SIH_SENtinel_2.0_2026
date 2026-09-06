from collections import Counter
from datetime import datetime, timezone

from app.core.config import settings
from app.models.network_traffic import NetworkTraffic


def _confidence(flows: list[NetworkTraffic]) -> float:
    if not flows:
        return 0.0
    timestamps = [flow.timestamp for flow in flows]
    span_days = max(0.0, (max(timestamps) - min(timestamps)).total_seconds() / 86400)
    quantity = min(1.0, len(flows) / max(20, settings.baseline_days * 4))
    coverage = min(1.0, span_days / max(1, settings.baseline_days))
    destinations = Counter(flow.destination_entity for flow in flows)
    consistency = max(destinations.values()) / len(flows)
    latest = max(timestamps).replace(tzinfo=timezone.utc) if max(timestamps).tzinfo is None else max(timestamps)
    recency = max(0.0, 1.0 - (datetime.now(timezone.utc) - latest).total_seconds() / (settings.baseline_days * 86400))
    return round(min(1.0, 0.35 * quantity + 0.25 * coverage + 0.25 * consistency + 0.15 * recency), 3)


def build_baseline(flows: list[NetworkTraffic], entity_id: str | None = None) -> dict:
    selected = [flow for flow in flows if entity_id is None or flow.source_entity == entity_id]
    relationships = Counter((flow.destination_entity, flow.protocol.upper(), flow.destination_port) for flow in selected)
    bytes_values = [flow.byte_count for flow in selected]
    return {
        "entity_id": entity_id,
        "sample_count": len(selected),
        "confidence": _confidence(selected),
        "common_relationships": [
            {"destination": destination, "protocol": protocol, "port": port, "frequency": count}
            for (destination, protocol, port), count in relationships.most_common(50)
        ],
        "protocols": sorted({flow.protocol.upper() for flow in selected}),
        "ports": sorted({flow.destination_port for flow in selected if flow.destination_port is not None}),
        "byte_volume": {"min": min(bytes_values, default=0), "max": max(bytes_values, default=0), "average": sum(bytes_values) / len(bytes_values) if bytes_values else 0},
    }


def relationship_evidence(flow: NetworkTraffic, baseline: dict) -> tuple[float, list[str]]:
    if baseline.get("sample_count", 0) == 0:
        return 100.0, []
    known = {(item["destination"], item["protocol"], item["port"]): item["frequency"] for item in baseline.get("common_relationships", [])}
    key = (flow.destination_entity, flow.protocol.upper(), flow.destination_port)
    if key in known:
        return min(100.0, 65.0 + min(35.0, known[key] * 5)), []
    return 25.0, ["NEW_RELATIONSHIP", "LOW_RELATIONSHIP_CONFIDENCE", "POSSIBLE_LATERAL_MOVEMENT"]
