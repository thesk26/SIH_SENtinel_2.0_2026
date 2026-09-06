from __future__ import annotations

from typing import Any

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from app.services.ml_forecasting_service import MODEL_FEATURES


class FeaturePreprocessor:
    def __init__(self, feature_names: tuple[str, ...] = MODEL_FEATURES) -> None:
        self.feature_names = tuple(feature_names)
        self.imputer = SimpleImputer(strategy="median", keep_empty_features=True)
        self.scaler = StandardScaler()

    def fit_transform(self, rows: list[dict[str, float | None]]) -> list[list[float]]:
        matrix = self._matrix(rows)
        return self.scaler.fit_transform(self.imputer.fit_transform(matrix)).tolist()

    def transform(self, rows: list[dict[str, Any]]) -> list[list[float]]:
        matrix = self._matrix(rows)
        return self.scaler.transform(self.imputer.transform(matrix)).tolist()

    def _matrix(self, rows: list[dict[str, Any]]) -> list[list[float | None]]:
        return [[self._value(row.get(name)) for name in self.feature_names] for row in rows]

    @staticmethod
    def _value(value: Any) -> float | None:
        if value in (None, "", "na", "n/a", "null", "none"):
            return None
        return float(bool(value)) if isinstance(value, bool) else float(value)
