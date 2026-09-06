from __future__ import annotations

import json
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from app.core.config import settings
from app.ml.preprocessing.dataset_loader import load_csv_dataset
from app.ml.preprocessing.feature_mapper import find_label_column, map_dataset, map_labels
from app.ml.preprocessing.feature_preprocessor import FeaturePreprocessor
from app.ml.training.model_evaluator import evaluate_model
from app.services.ml_forecasting_service import MODEL_FEATURES

SUPPORTED_CLASSES = {"NORMAL", "PORT_SCAN", "BRUTE_FORCE", "LATERAL_MOVEMENT", "DOS_OR_DDOS", "DATA_EXFILTRATION"}


def train_model(dataset_path: Path, output_path: Path) -> dict[str, Any]:
    rows, headers = load_csv_dataset(dataset_path)
    label_column = find_label_column(headers)
    mapped_rows, missing_features = map_dataset(rows, headers)
    labels = map_labels(rows, label_column)
    unknown_labels = sorted(set(labels) - SUPPORTED_CLASSES)
    if unknown_labels:
        raise ValueError(f"Unsupported attack labels: {', '.join(unknown_labels)}")
    if len(rows) < 8:
        raise ValueError("At least eight labelled rows are required for a reproducible train/test split")
    preprocessor = FeaturePreprocessor()
    matrix = preprocessor.fit_transform(mapped_rows)
    test_size = max(2, round(len(labels) * 0.25))
    if len(labels) - test_size < 2:
        raise ValueError("Dataset is too small after reserving the test set")
    counts = {label: labels.count(label) for label in set(labels)}
    stratify = labels if min(counts.values()) >= 2 and test_size >= len(counts) else None
    x_train, x_test, y_train, y_test = train_test_split(matrix, labels, test_size=test_size, random_state=42, stratify=stratify)
    model = RandomForestClassifier(n_estimators=150, max_features="sqrt", random_state=42, class_weight="balanced", min_samples_leaf=2)
    model.fit(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test)
    report: dict[str, Any] = {
        "model": "RandomForestClassifier",
        "model_name": "RandomForestClassifier",
        "model_version": settings.model_version,
        "preprocessing_version": settings.preprocessing_version,
        "training_date": datetime.now(timezone.utc).isoformat(),
        "dataset_name": dataset_path.name,
        **metrics,
        "training_samples": len(x_train),
        "testing_samples": len(x_test),
        "classes": list(model.classes_),
        "feature_names": list(MODEL_FEATURES),
        "feature_types": {name: "float" for name in MODEL_FEATURES},
        "mapped_columns": {name: name not in missing_features for name in MODEL_FEATURES},
        "label_column": label_column,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as model_file:
        pickle.dump({"model": model, "classes": list(model.classes_), "features": MODEL_FEATURES, "preprocessor": preprocessor, "metrics": report, "metadata": {"model_name": report["model_name"], "model_version": report["model_version"], "preprocessing_version": report["preprocessing_version"], "training_date": report["training_date"], "dataset_name": report["dataset_name"], "feature_order": list(MODEL_FEATURES), "feature_types": report["feature_types"], "supported_classes": report["classes"]}}, model_file)
    _write_json(output_path.with_name("model_metrics.json"), report)
    _write_json(output_path.with_name("feature_metadata.json"), {"model_name": report["model_name"], "model_version": report["model_version"], "features": list(MODEL_FEATURES), "feature_order": list(MODEL_FEATURES), "feature_types": report["feature_types"], "preprocessing_version": settings.preprocessing_version, "missing_dataset_features": missing_features, "label_column": label_column})
    return report


def _write_json(path: Path, value: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as report_file:
        json.dump(value, report_file, indent=2)
