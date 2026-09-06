from __future__ import annotations

import json
import re
from pathlib import Path

from app.core.config import settings

UNKNOWN_LABEL = "UNKNOWN"
SUPPORTED_LABELS = ("NORMAL", "PORT_SCAN", "BRUTE_FORCE", "LATERAL_MOVEMENT", "DOS_OR_DDOS", "DATA_EXFILTRATION", UNKNOWN_LABEL)


def _token(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", " ", value.strip().upper()).strip()


def load_label_mappings(path: Path | None = None) -> dict[str, set[str]]:
    mapping_path = path or Path(__file__).parents[1] / "config" / "label_mappings.json"
    with mapping_path.open(encoding="utf-8") as mapping_file:
        raw = json.load(mapping_file)
    return {str(target): {_token(alias) for alias in aliases} | {_token(target)} for target, aliases in raw.items()}


def normalize_label(raw_label: str, mappings: dict[str, set[str]] | None = None) -> str:
    value = _token(raw_label)
    for target, aliases in (mappings or load_label_mappings()).items():
        if value in aliases:
            return target
    return UNKNOWN_LABEL
