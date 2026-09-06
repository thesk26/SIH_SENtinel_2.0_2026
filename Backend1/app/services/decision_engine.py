from dataclasses import dataclass
from enum import StrEnum

from app.core.config import settings


class Decision(StrEnum):
    PASS = "PASS"
    MONITOR = "MONITOR"
    CHALLENGE = "CHALLENGE"
    ISOLATE = "ISOLATE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class DecisionResult:
    decision: Decision
    reason: str


def decide(integrity_score: float, conflicts: list[str], critical_conflicts: set[str] | None = None) -> DecisionResult:
    critical_conflicts = critical_conflicts or {"SUSPICIOUS_NETWORK", "MULTI_SIGNAL_CRITICAL"}
    if "POSSIBLE_LATERAL_MOVEMENT" in conflicts and integrity_score < settings.pass_threshold:
        return DecisionResult(Decision.ISOLATE, "Potential lateral movement requires device isolation")
    if len(set(conflicts).intersection(critical_conflicts)) >= 1 or len(conflicts) >= 4:
        return DecisionResult(Decision.BLOCK, "Critical or widespread assumption conflicts detected")
    if integrity_score >= settings.pass_threshold:
        return DecisionResult(Decision.PASS, "Signals are consistent with the established baseline")
    if integrity_score >= settings.challenge_threshold:
        return DecisionResult(Decision.CHALLENGE, "Additional verification is required")
    return DecisionResult(Decision.BLOCK, "Integrity score is below the blocking threshold")
