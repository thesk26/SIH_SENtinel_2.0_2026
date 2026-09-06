from __future__ import annotations

import pickle
from threading import Lock
from pathlib import Path
from typing import Any

from app.core.config import settings

MODEL_FEATURES = (
    "unique_destinations",
    "connection_frequency",
    "port_diversity",
    "protocol_diversity",
    "packet_volume",
    "byte_volume",
    "traffic_spike",
    "repeated_failures",
    "rapid_connections",
    "flow_duration_ms",
)
SUPPORTED_CLASSES = {"NORMAL", "PORT_SCAN", "BRUTE_FORCE", "LATERAL_MOVEMENT", "DOS_OR_DDOS", "DATA_EXFILTRATION"}
_MODEL_LOCK = Lock()
_MODEL_STATE: dict[str, Any] = {"path": None, "mtime": None, "artifact": None, "error": None}


def feature_vector(features: dict[str, Any]) -> list[float]:
    return [float(bool(features.get(name))) if name in {"traffic_spike", "rapid_connections"} else float(features.get(name, 0.0)) for name in MODEL_FEATURES]


def _load_model(path_value: str) -> dict[str, Any] | None:
    path = Path(path_value)
    if not path.is_file():
        return _MODEL_STATE["artifact"] if _MODEL_STATE["path"] == path_value else None
    mtime = path.stat().st_mtime_ns
    if _MODEL_STATE["path"] == path_value and _MODEL_STATE["mtime"] == mtime:
        return _MODEL_STATE["artifact"]
    try:
        with _MODEL_LOCK:
            with path.open("rb") as model_file:
                artifact = pickle.load(model_file)
            if not isinstance(artifact, dict) or "model" not in artifact or "classes" not in artifact:
                raise ValueError("ML artifact must contain model and classes")
            _MODEL_STATE.update({"path": path_value, "mtime": mtime, "artifact": artifact, "error": None})
            return artifact
    except (OSError, ValueError, pickle.PickleError, EOFError, AttributeError, ImportError) as error:
        _MODEL_STATE["error"] = str(error)
        return _MODEL_STATE["artifact"]


def model_status() -> dict[str, Any]:
    artifact = _load_model(settings.ml_model_path)
    return {"loaded": artifact is not None, "path": settings.ml_model_path, "version": (artifact or {}).get("metadata", {}).get("model_version"), "error": _MODEL_STATE["error"]}


def predict(features: dict[str, Any]) -> dict[str, Any]:
    artifact = _load_model(settings.ml_model_path)
    if artifact is None:
        return {"available": False, "forecast_source": "RULE_BASED_FALLBACK", "ml_model_loaded": False, "probabilities": {}, "confidence_level": "LOW", "top_class": None, "top_probability": 0.0}
    model = artifact["model"]
    try:
        artifact_features = tuple(artifact.get("features", ()))
        classes = [str(value) for value in artifact["classes"]]
        if artifact_features != MODEL_FEATURES or not classes or not set(classes).issubset(SUPPORTED_CLASSES):
            raise ValueError("ML artifact metadata is incompatible with SENTINAL")
        preprocessor = artifact.get("preprocessor")
        if preprocessor is not None and tuple(preprocessor.feature_names) != MODEL_FEATURES:
            raise ValueError("ML preprocessor feature metadata is incompatible with SENTINAL")
        vector = preprocessor.transform([features]) if preprocessor is not None else [feature_vector(features)]
        probabilities = model.predict_proba(vector)[0]
        if len(classes) != len(probabilities):
            raise ValueError("ML artifact classes do not match model probabilities")
        probability_map = {label: round(float(probability), 4) for label, probability in zip(classes, probabilities)}
        top_class, top_probability = max(probability_map.items(), key=lambda item: item[1])
        if top_probability >= settings.high_confidence_threshold:
            confidence_level = "HIGH"
        elif top_probability >= settings.medium_confidence_threshold:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        return {"available": True, "forecast_source": "ML_MODEL", "ml_model_loaded": True, "probabilities": probability_map, "confidence_level": confidence_level, "top_class": top_class, "top_probability": top_probability}
    except (AttributeError, IndexError, TypeError, ValueError):
        return {"available": False, "forecast_source": "RULE_BASED_FALLBACK", "ml_model_loaded": False, "probabilities": {}, "confidence_level": "LOW", "top_class": None, "top_probability": 0.0}
