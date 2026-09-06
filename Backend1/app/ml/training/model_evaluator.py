from __future__ import annotations

from typing import Any

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def evaluate_model(model: Any, features: list[list[float]], labels: list[str]) -> dict[str, float]:
    predictions = model.predict(features)
    return {
        "accuracy": round(float(accuracy_score(labels, predictions)), 6),
        "precision": round(float(precision_score(labels, predictions, average="weighted", zero_division=0)), 6),
        "recall": round(float(recall_score(labels, predictions, average="weighted", zero_division=0)), 6),
        "f1_score": round(float(f1_score(labels, predictions, average="weighted", zero_division=0)), 6),
    }
