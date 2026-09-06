from collections import Counter

from app.models.network_traffic import NetworkTraffic


def extract_features(flow: NetworkTraffic, recent_flows: list[NetworkTraffic]) -> dict[str, float | bool]:
    source_flows = [item for item in recent_flows if item.source_entity == flow.source_entity]
    destinations = {item.destination_entity for item in source_flows}
    ports = {item.destination_port for item in source_flows if item.destination_port is not None}
    protocols = {item.protocol.upper() for item in source_flows}
    failures = sum(item.connection_status.lower() not in {"success", "accepted", "established"} for item in source_flows)
    bytes_seen = sum(item.byte_count for item in source_flows)
    return {
        "unique_destinations": float(len(destinations)),
        "connection_frequency": float(len(source_flows)),
        "port_diversity": float(len(ports)),
        "protocol_diversity": float(len(protocols)),
        "packet_volume": float(sum(item.packet_count for item in source_flows)),
        "byte_volume": float(bytes_seen),
        "traffic_spike": bool(source_flows and flow.byte_count > max(1, bytes_seen / len(source_flows)) * 3),
        "repeated_failures": float(failures),
        "rapid_connections": bool(flow.request_frequency >= 20),
        "flow_duration_ms": float(getattr(flow, "flow_duration_ms", 0)),
        "top_ports": [port for port, _ in Counter(item.destination_port for item in source_flows).most_common(5) if port is not None],
    }
