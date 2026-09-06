from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.services.ml_forecasting_service import MODEL_FEATURES

FEATURE_MAPPING: dict[str, tuple[str, ...]] = {
    "unique_destinations": ("unique_destinations", "distinct_destinations", "destination_count", "dst_ip_count"),
    "connection_frequency": ("connection_frequency", "flow_count", "connections", "connection_count"),
    "port_diversity": ("port_diversity", "distinct_ports", "destination_port_count", "dst_port_count"),
    "protocol_diversity": ("protocol_diversity", "distinct_protocols", "protocol_count"),
    "packet_volume": ("packet_volume", "packets_per_minute", "total_packets", "tot_pkts", "packet_count", "packets"),
    "byte_volume": ("byte_volume", "bytes_per_minute", "total_bytes", "tot_bytes", "bytes", "flow_bytes", "byte_count"),
    "traffic_spike": ("traffic_spike", "is_spike", "spike"),
    "repeated_failures": ("repeated_failures", "failed_connections", "failure_count", "retries"),
    "rapid_connections": ("rapid_connections", "rapid_attempts", "connection_rate", "request_frequency", "connections_per_minute"),
    "flow_duration_ms": ("flow_duration_ms", "duration_ms", "duration", "flow_duration"),
}

LABEL_COLUMNS = ("label", "attack_type", "class", "target", "subcategory")


def load_feature_mapping(path: Path | None = None) -> dict[str, tuple[str, ...]]:
    mapping_path = path or Path(__file__).parents[1] / "config" / "feature_mappings.json"
    with mapping_path.open(encoding="utf-8") as mapping_file:
        raw = json.load(mapping_file)
    return {str(feature): tuple(str(alias) for alias in aliases) for feature, aliases in raw.items()}


def _number(value: Any, feature: str, row_number: int) -> float | None:
    if value in (None, "", "na", "n/a", "null", "none"):
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, str) and value.lower() in {"true", "yes"}:
        return 1.0
    if isinstance(value, str) and value.lower() in {"false", "no"}:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Feature '{feature}' at row {row_number} is not numeric: {value!r}") from error


def map_dataset(rows: list[dict[str, Any]], headers: list[str], mapping: dict[str, tuple[str, ...]] | None = None) -> tuple[list[dict[str, float | None]], list[str]]:
    mapping = mapping or load_feature_mapping()
    available = set(headers)
    selected: dict[str, str] = {}
    for feature in MODEL_FEATURES:
        candidate = next((name for name in mapping.get(feature, ()) if name in available), None)
        if candidate:
            selected[feature] = candidate
    if not selected:
        raise ValueError("Dataset has no supported SENTINAL feature columns; provide a feature mapping for this dataset")
    mapped: list[dict[str, float | None]] = []
    for row_number, row in enumerate(rows, start=2):
        mapped.append({feature: _number(row.get(selected[feature]), feature, row_number) if feature in selected else None for feature in MODEL_FEATURES})
    return mapped, [feature for feature in MODEL_FEATURES if feature not in selected]


def find_label_column(headers: list[str]) -> str:
    label = next((name for name in LABEL_COLUMNS if name in headers), None)
    if label is None:
        raise ValueError(f"Dataset must contain one label column: {', '.join(LABEL_COLUMNS)}")
    return label


def map_labels(rows: list[dict[str, Any]], label_column: str) -> list[str]:
    from app.ml.preprocessing.label_normalizer import normalize_label

    labels = [normalize_label(str(row.get(label_column, ""))) for row in rows]
    if any(not label for label in labels):
        raise ValueError(f"Label column '{label_column}' contains empty values")
    if "UNKNOWN" in labels:
        raise ValueError("Dataset contains labels that could not be confidently normalized: UNKNOWN")
    if len(set(labels)) < 2:
        raise ValueError("At least two attack classes are required")
    return labels
