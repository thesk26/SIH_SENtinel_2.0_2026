from __future__ import annotations


def recommendations(decision: str, conflicts: list[str], forecast: dict) -> list[str]:
    actions = ["Monitor the affected endpoint"]
    if "NEW_RELATIONSHIP" in conflicts:
        actions.append("Investigate the new internal relationship")
    if forecast.get("attack_path", {}).get("attack_path_detected"):
        actions.append("Restrict unnecessary access along the predicted attack path")
    if forecast.get("predicted_attack_type") in {"BRUTE_FORCE", "POSSIBLE_PORT_SCAN"}:
        actions.append("Review authentication and connection-attempt logs")
    if decision in {"BLOCK", "ISOLATE"}:
        actions.append("Contain the affected endpoint through the approved response process")
    return list(dict.fromkeys(actions))
