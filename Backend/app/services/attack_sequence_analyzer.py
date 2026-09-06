from collections.abc import Iterable


def _contains_in_order(events: list[tuple[str, object]], pattern: tuple[str, ...]) -> list[int]:
    positions: list[int] = []
    next_position = 0
    for expected in pattern:
        match = next((index for index in range(next_position, len(events)) if events[index][0] == expected), None)
        if match is None:
            return []
        positions.append(match)
        next_position = match + 1
    return positions


def _events_for_flow(flow) -> list[str]:
    features = flow.derived_features or {}
    conflicts = set(features.get("conflicts", []))
    events: list[str] = []
    if features.get("rapid_connections"):
        events.append("RAPID_CONNECTION_ATTEMPTS")
    if features.get("port_diversity", 0) >= 3:
        events.append("MULTIPLE_DESTINATION_PORTS")
    if features.get("repeated_failures", 0) >= 3:
        events.append("MULTIPLE_FAILED_CONNECTIONS")
    if "NEW_RELATIONSHIP" in conflicts:
        events.append("NEW_RELATIONSHIP")
    if features.get("unique_destinations", 0) >= 2:
        events.append("MULTIPLE_INTERNAL_CONNECTIONS")
    if "NEW_RELATIONSHIP" in conflicts and flow.destination_port in {22, 23, 445, 3389, 5432, 3306, 1433}:
        events.append("UNUSUAL_SERVICE_ACCESS")
    if flow.byte_count >= 1_000_000:
        events.append("LARGE_OUTBOUND_TRANSFER")
    if features.get("byte_volume", 0) >= 2_000_000:
        events.append("SUSTAINED_HIGH_VOLUME_TRAFFIC")
    return events


def analyze_sequence(flows: Iterable) -> dict:
    ordered = sorted(flows, key=lambda item: item.timestamp)
    observed: list[tuple[str, object]] = []
    targets: set[str] = set()
    for flow in ordered:
        targets.add(flow.destination_entity)
        for event in _events_for_flow(flow):
            observed.append((event, flow.timestamp))

    patterns = (
        ("POSSIBLE_RECONNAISSANCE", ("RAPID_CONNECTION_ATTEMPTS", "MULTIPLE_DESTINATION_PORTS", "MULTIPLE_FAILED_CONNECTIONS")),
        ("POSSIBLE_BRUTE_FORCE", ("RAPID_CONNECTION_ATTEMPTS", "MULTIPLE_FAILED_CONNECTIONS")),
        ("POSSIBLE_LATERAL_MOVEMENT", ("NEW_RELATIONSHIP", "MULTIPLE_INTERNAL_CONNECTIONS", "UNUSUAL_SERVICE_ACCESS")),
        ("POSSIBLE_DATA_EXFILTRATION", ("NEW_RELATIONSHIP", "LARGE_OUTBOUND_TRANSFER", "SUSTAINED_HIGH_VOLUME_TRAFFIC")),
    )
    selected_type = "NO_CLEAR_ATTACK_PROGRESSION"
    event_order: list[int] = []
    for sequence_type, pattern in patterns:
        positions = _contains_in_order(observed, pattern)
        if positions:
            selected_type = sequence_type
            event_order = [position + 1 for position in positions]
            break
    confidence = min(0.98, 0.25 + len(event_order) * 0.18 + max(0, len(observed) - len(event_order)) * 0.03)
    return {
        "sequence_detected": bool(event_order),
        "sequence_type": selected_type,
        "sequence_confidence": round(confidence, 3) if event_order else 0.0,
        "events": [event for event, _ in observed],
        "event_order": event_order,
        "event_count": len(observed),
        "potential_targets": sorted(targets),
        "flow_count": len(ordered),
    }
