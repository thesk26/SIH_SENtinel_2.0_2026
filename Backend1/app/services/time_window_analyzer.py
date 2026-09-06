from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Iterable


def _timestamp(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def _flow_key(flow) -> tuple:
    identifier = getattr(flow, "id", None)
    if identifier:
        return ("id", identifier)
    source_identifier = getattr(flow, "source_event_id", None)
    if source_identifier:
        return ("source_event_id", source_identifier)
    fingerprint = getattr(flow, "event_fingerprint", None)
    if fingerprint:
        return ("fingerprint", fingerprint)
    return ("flow", getattr(flow, "source_entity", None), getattr(flow, "destination_entity", None), getattr(flow, "timestamp", None), getattr(flow, "protocol", None), getattr(flow, "source_port", None), getattr(flow, "destination_port", None), getattr(flow, "byte_count", None), getattr(flow, "packet_count", None), getattr(flow, "connection_status", None))


def select_window(flows: Iterable, window_minutes: int, reference_time: datetime | None = None) -> list:
    unique = {_flow_key(flow): flow for flow in flows}
    ordered = sorted(unique.values(), key=lambda flow: _timestamp(flow.timestamp))
    if not ordered:
        return []
    end = _timestamp(reference_time or ordered[-1].timestamp)
    start = end - timedelta(minutes=window_minutes)
    return [flow for flow in ordered if start <= _timestamp(flow.timestamp) <= end]


def aggregate_window(flows: Iterable, window_minutes: int, reference_time: datetime | None = None, baseline_flows: Iterable | None = None) -> dict[str, float | bool | int | list]:
    selected = select_window(flows, window_minutes, reference_time)
    divisor = max(1.0, float(window_minutes))
    destinations = {flow.destination_entity for flow in selected}
    ports = {flow.destination_port for flow in selected if flow.destination_port is not None}
    protocols = {str(flow.protocol).upper() for flow in selected}
    failures = sum(str(flow.connection_status).lower() not in {"success", "accepted", "established"} for flow in selected)
    baseline = list(baseline_flows or [])
    baseline_destinations = {flow.destination_entity for flow in baseline}
    baseline_ports = {flow.destination_port for flow in baseline if flow.destination_port is not None}
    baseline_protocols = {str(flow.protocol).upper() for flow in baseline}
    new_destinations = sorted(destinations - baseline_destinations)
    new_ports = sorted(ports - baseline_ports)
    new_protocols = sorted(protocols - baseline_protocols)
    return {
        "window_minutes": window_minutes,
        "flow_count": len(selected),
        "unique_destinations": float(len(destinations)),
        "connection_frequency": len(selected) / divisor,
        "port_diversity": float(len(ports)),
        "protocol_diversity": float(len(protocols)),
        "packet_volume": sum(flow.packet_count for flow in selected) / divisor,
        "byte_volume": sum(flow.byte_count for flow in selected) / divisor,
        "connections_per_minute": len(selected) / divisor,
        "packets_per_minute": sum(flow.packet_count for flow in selected) / divisor,
        "bytes_per_minute": sum(flow.byte_count for flow in selected) / divisor,
        "unique_destinations_in_window": float(len(destinations)),
        "unique_ports_in_window": float(len(ports)),
        "unique_protocols_in_window": float(len(protocols)),
        "new_destinations_against_baseline": new_destinations,
        "new_destination_count": len(new_destinations),
        "new_ports_against_baseline": new_ports,
        "new_port_count": len(new_ports),
        "new_protocols_against_baseline": new_protocols,
        "new_protocol_count": len(new_protocols),
        "failed_connections_per_window": float(failures),
        "traffic_spike": any(bool((flow.derived_features or {}).get("traffic_spike")) for flow in selected),
        "repeated_failures": float(failures),
        "rapid_connections": any(bool((flow.derived_features or {}).get("rapid_connections")) for flow in selected),
        "flow_duration_ms": sum(getattr(flow, "flow_duration_ms", 0) for flow in selected) / max(1, len(selected)),
    }
