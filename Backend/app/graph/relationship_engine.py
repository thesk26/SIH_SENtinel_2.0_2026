from app.graph.assumption_graph import AssumptionGraph


def relationship_integrity(graph: AssumptionGraph, conflicts: list[str]) -> float:
    if not graph.nodes:
        return max(0.0, 50.0 - min(50.0, len(conflicts) * 12.0))
    confidence = sum(node.confidence for node in graph.nodes) / len(graph.nodes)
    conflict_penalty = min(50.0, len(conflicts) * 12.0)
    return max(0.0, min(100.0, confidence * 100.0 - conflict_penalty))


def relationship_graph_score(graph: AssumptionGraph, relationship_key: str, conflicts: list[str]) -> float:
    matching = [node for node in graph.nodes if node.reference == relationship_key]
    if not matching:
        return relationship_integrity(graph, [*conflicts, "NEW_RELATIONSHIP"])
    return relationship_integrity(AssumptionGraph(graph.user_id, matching), conflicts)
