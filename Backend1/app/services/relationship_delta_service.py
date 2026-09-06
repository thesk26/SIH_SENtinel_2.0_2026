from __future__ import annotations

from collections import Counter


def relationship_deltas(current_flows: list, baseline_flows: list) -> dict:
    source_entities = {flow.source_entity for flow in current_flows}
    baseline_flows = [flow for flow in baseline_flows if flow.source_entity in source_entities]
    current = Counter((flow.destination_entity, flow.destination_port, str(flow.protocol).upper()) for flow in current_flows)
    historical = Counter((flow.destination_entity, flow.destination_port, str(flow.protocol).upper()) for flow in baseline_flows)
    current_destinations = {key[0] for key in current}
    historical_destinations = {key[0] for key in historical}
    current_ports = {key[1] for key in current if key[1] is not None}
    historical_ports = {key[1] for key in historical if key[1] is not None}
    current_protocols = {key[2] for key in current}
    historical_protocols = {key[2] for key in historical}
    return {
        "new_destinations": sorted(current_destinations - historical_destinations),
        "new_ports": sorted(current_ports - historical_ports),
        "new_protocols": sorted(current_protocols - historical_protocols),
        "new_relationships": [
            {"destination": destination, "port": port, "protocol": protocol, "frequency": count}
            for (destination, port, protocol), count in current.items()
            if (destination, port, protocol) not in historical
        ],
        "frequency_changes": [
            {"destination": key[0], "port": key[1], "protocol": key[2], "previous": historical[key], "current": current[key]}
            for key in current
            if key in historical and current[key] != historical[key]
        ],
    }
