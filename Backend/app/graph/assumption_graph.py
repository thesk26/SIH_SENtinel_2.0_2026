from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AssumptionNode:
    kind: str
    reference: str
    confidence: float
    frequency: float
    consistency: float
    last_observed: datetime | None = None
    risk_weight: float = 1.0


@dataclass
class AssumptionGraph:
    """In-memory graph boundary designed for a future Neo4j adapter."""

    user_id: str
    nodes: list[AssumptionNode] = field(default_factory=list)

    def add(self, node: AssumptionNode) -> None:
        self.nodes.append(node)

    def by_kind(self, kind: str) -> list[AssumptionNode]:
        return [node for node in self.nodes if node.kind == kind]
