import csv
import pickle

import pytest

from app.ml.preprocessing.dataset_loader import load_csv_dataset
from app.ml.preprocessing.feature_mapper import find_label_column, map_dataset, map_labels
from app.ml.preprocessing.label_normalizer import normalize_label
from app.ml.training.model_trainer import train_model
from app.services.forecasting_engine import forecast
from app.services.ml_forecasting_service import MODEL_FEATURES, predict


def write_dataset(path, rows: int = 8) -> None:
	with path.open("w", newline="", encoding="utf-8") as dataset_file:
		writer = csv.DictWriter(dataset_file, fieldnames=["total_packets", "total_bytes", "duration", "rapid_attempts", "attack_type"])
		writer.writeheader()
		for index in range(rows):
			writer.writerow({"total_packets": index + 1, "total_bytes": (index + 1) * 100, "duration": 50, "rapid_attempts": "false", "attack_type": "NORMAL" if index < rows // 2 else "PORT_SCAN"})


def test_dataset_loader_normalizes_headers_and_maps_aliases(tmp_path) -> None:
	dataset = tmp_path / "flows.csv"
	write_dataset(dataset)
	rows, headers = load_csv_dataset(dataset)
	mapped, missing = map_dataset(rows, headers)
	assert "total_packets" in headers
	assert mapped[0]["packet_volume"] == 1
	assert "byte_volume" not in missing
	assert map_labels(rows, find_label_column(headers))[0] == "NORMAL"


def test_unsupported_dataset_fails_clearly(tmp_path) -> None:
	dataset = tmp_path / "unsupported.csv"
	dataset.write_text("foo,attack_type\nbar,NORMAL\n", encoding="utf-8")
	rows, headers = load_csv_dataset(dataset)
	with pytest.raises(ValueError, match="no supported SENTINAL feature"):
		map_dataset(rows, headers)


def test_training_saves_artifact_and_metrics(tmp_path) -> None:
	dataset = tmp_path / "flows.csv"
	artifact = tmp_path / "network_forecast_model.pkl"
	write_dataset(dataset, rows=12)
	report = train_model(dataset, artifact)
	assert artifact.is_file()
	assert (tmp_path / "model_metrics.json").is_file()
	assert set(("accuracy", "precision", "recall", "f1_score")).issubset(report)


def test_trained_artifact_uses_shared_preprocessor(monkeypatch, tmp_path) -> None:
	from app.core import config

	dataset = tmp_path / "flows.csv"
	artifact = tmp_path / "network_forecast_model.pkl"
	write_dataset(dataset, rows=12)
	train_model(dataset, artifact)
	monkeypatch.setattr(config.settings, "ml_model_path", str(artifact))
	result = predict({name: 0 for name in MODEL_FEATURES})
	assert result["ml_model_loaded"] is True
	assert result["confidence_level"] in {"HIGH", "MEDIUM", "LOW"}
	assert result["probabilities"]


def test_mismatched_feature_metadata_uses_fallback(monkeypatch, tmp_path) -> None:
	from app.core import config

	artifact = tmp_path / "bad.pkl"
	with artifact.open("wb") as artifact_file:
		pickle.dump({"model": object(), "classes": ["NORMAL"], "features": ("wrong_feature",)}, artifact_file)
	monkeypatch.setattr(config.settings, "ml_model_path", str(artifact))
	result = predict({name: 0 for name in MODEL_FEATURES})
	assert result["ml_model_loaded"] is False
	assert result["forecast_source"] == "RULE_BASED_FALLBACK"


def test_missing_model_uses_truthful_fallback(monkeypatch, tmp_path) -> None:
	from app.core import config
	monkeypatch.setattr(config.settings, "ml_model_path", str(tmp_path / "missing.pkl"))
	result = predict({name: 0 for name in MODEL_FEATURES})
	assert result["available"] is False
	assert result["forecast_source"] == "RULE_BASED_FALLBACK"
	assert result["ml_model_loaded"] is False


def test_empty_forecast_has_no_fake_probability() -> None:
	result = forecast([])
	assert result["forecast_available"] is False
	assert result["attack_probability"] is None
	assert result["predicted_attack_type"] == "NO_DATA"


def test_dataset_labels_are_normalized() -> None:
	assert normalize_label("BENIGN") == "NORMAL"
	assert normalize_label("PortScan") == "PORT_SCAN"
	assert normalize_label("DDoS") == "DOS_OR_DDOS"
	assert normalize_label("something-unclassified") == "UNKNOWN"
