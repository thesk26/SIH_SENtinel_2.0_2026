from app.services.decision_engine import Decision


def explain(decision: Decision, conflicts: list[str], level: str = "USER_SAFE") -> dict:
    if level == "USER_SAFE":
        messages = {
            Decision.PASS: "Activity is consistent with your recent security profile.",
            Decision.MONITOR: "Minor anomalies were detected and will be monitored.",
            Decision.CHALLENGE: "We detected unusual activity and require additional verification.",
            Decision.ISOLATE: "Potentially unsafe network activity was isolated for protection.",
            Decision.BLOCK: "This activity was blocked for your protection.",
        }
        return {"level": level, "message": messages[decision]}
    readable = [conflict.replace("_", " ").title() for conflict in conflicts]
    return {
        "level": level,
        "message": "Security decision generated from observable signal inconsistencies.",
        "reasons": readable,
    }
