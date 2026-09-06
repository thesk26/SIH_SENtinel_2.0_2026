from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ThreatIntelMatch:
    indicator: str
    matched: bool
    source: str
    confidence: float
    observed_at: datetime


class ThreatIntelligenceProvider(Protocol):
    def lookup(self, indicator: str) -> ThreatIntelMatch: ...


class LocalThreatIntelligenceProvider:
    def __init__(self, indicators: dict[str, float] | None = None) -> None:
        self.indicators = indicators if indicators is not None else self._load_demo_indicators()

    @staticmethod
    def _load_demo_indicators() -> dict[str, float]:
        path = Path(__file__).parents[1] / "data" / "demo_threat_indicators.json"
        try:
            with path.open(encoding="utf-8") as indicator_file:
                raw = json.load(indicator_file)
            return {key: float(value["confidence"]) for key, value in raw.items() if not key.startswith("_")}
        except (OSError, ValueError, KeyError, TypeError):
            return {}

    def lookup(self, indicator: str) -> ThreatIntelMatch:
        confidence = self.indicators.get(indicator, 0.0)
        return ThreatIntelMatch(indicator, confidence > 0, "LOCAL_THREAT_DATABASE", confidence, datetime.now(timezone.utc))
