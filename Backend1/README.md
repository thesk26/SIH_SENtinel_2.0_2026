# SENTINAL

SENTINAL is a network-intelligence and assumption-integrity API. It learns privacy-preserving traffic metadata, detects relationship and behavioral violations, and produces evidence-based attack forecasts. Existing authentication and behavioral analysis remain supported.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload
```

The API and Swagger UI are available at `http://localhost:8000/docs`. SQLite is the default local database. Set `DATABASE_URL` to PostgreSQL for deployment.

## API flow

1. Register and login at `/api/auth/register` and `/api/auth/login`.
2. Send anonymized metrics to `/api/behavior/collect` during the configurable learning period.
3. Analyze current signals at `/api/security/analyze`.
4. Read the current user's events at `/api/security/events`.
5. Submit flow metadata to `/api/network/traffic` or analyze it at `/api/network/analyze`.
6. Generate a forecast at `/api/security/forecast` and retrieve it by ID.
7. Request labeled simulated input from `/api/network/demo` for a controlled demonstration.
8. Inspect `/api/dashboard/summary`, `/api/dashboard/timeline`, `/api/dashboard/risk`, and `/api/dashboard/attack-path` with an authenticated token.

The operational health endpoints are `/health` and `/system/health`. They report database readiness and whether a compatible ML artifact is loaded without exposing secrets.

Device fingerprints and network identifiers are SHA-256 hashed before persistence. Raw keystrokes are never accepted or stored. JWT access and refresh tokens are supported. Authentication and security routes include rate limiting; local development uses an in-memory limiter, while multi-worker deployments can inject the included `RedisRateLimiter` adapter and a managed secret.

## Tests

```powershell
pytest -q
```

The scoring engine is intentionally transparent and configurable. It is a risk signal, not proof of identity or an assertion that behavioral analysis can perfectly identify an attacker.

## Configuration

Set `SECRET_KEY` to a randomly generated value of at least 16 characters. Set `DATABASE_URL` to a managed PostgreSQL URL in deployment; SQLite is suitable for local development. `BASELINE_DAYS`, `BASELINE_UPDATE_THRESHOLD`, `PASS_THRESHOLD`, `CHALLENGE_THRESHOLD`, hybrid forecast weights, and `CORS_ORIGINS` are configurable through the `.env` file. Flow entity identifiers are SHA-256 hashed, and raw packet payloads are never accepted or stored.

## Dataset preparation and ML model

The application uses the explainable rule-based forecast until a compatible trained artifact exists. Place a public or privately licensed CSV outside the source package, for example under `datasets/`. Do not commit datasets or trained artifacts unless they are intentionally approved for redistribution.

The loader normalizes headers and maps common aliases such as `total_packets`, `tot_pkts`, and `packet_count` to `packet_volume`; `total_bytes`, `bytes`, and `flow_bytes` to `byte_volume`; `duration` and `flow_duration` to `flow_duration_ms`; and `rapid_attempts` or `request_frequency` to `rapid_connections`. A label column named `label`, `attack_type`, `class`, `target`, or `subcategory` is required. Unsupported datasets fail with a clear error; unavailable mapped features are explicitly recorded and imputed by the saved preprocessing pipeline.

Feature aliases are configured in `app/ml/config/feature_mappings.json`. Labels are normalized through `app/ml/config/label_mappings.json`; uncertain labels become `UNKNOWN` and are rejected from training rather than silently assigned to an attack class.

Train a Random Forest model with:

```powershell
python train_model.py --dataset path\to\network_flows.csv
```

The command writes the model artifact to `ML_MODEL_PATH` and also generates `model_metrics.json` and `feature_metadata.json` beside it. Metrics are calculated from the held-out test split and include accuracy, weighted precision, weighted recall, and weighted F1. Supported labels are `NORMAL`, `PORT_SCAN`, `BRUTE_FORCE`, `LATERAL_MOVEMENT`, `DOS_OR_DDOS`, and `DATA_EXFILTRATION`. The saved imputer/scaler is loaded for inference so training and runtime feature order remain identical.

Model metadata records the actual model name/version, preprocessing version, training date, dataset filename, sample counts, feature order/types, supported classes, and measured metrics. Inference rejects incompatible metadata and uses the rule-based fallback.

## Analysis pipeline

Traffic metadata is validated and stored, then transformed into communication, volume, frequency, and failure features. Adaptive baselines measure relationship frequency, ports, protocols, time coverage, recency, and consistency. Relationship violations become integrity conflicts; recent conflicts are ordered into attack sequences, which produce a probability, confidence, predicted progression, targets, risk level, and explanation. A forecast is an estimate, not proof of an attack.

Forecast features use the configurable `DEFAULT_ANALYSIS_WINDOW_MINUTES` window. Duplicate flow keys are removed, boundary timestamps are included, and traffic is represented as connections, packets, and bytes per minute plus new destinations, new ports, and failed connections in the selected window. Effective hybrid weights are renormalized over available components; low-confidence ML output is downweighted before sequence, relationship, and integrity evidence are combined.

Window output distinguishes `unique_destinations_in_window`, `unique_ports_in_window`, and `unique_protocols_in_window` from `new_destinations_against_baseline`, `new_ports_against_baseline`, and `new_protocols_against_baseline`. A single new protocol or relationship is evidence, not an automatic block decision.

Analyzed flows are retained for audit, but only flows above `BASELINE_UPDATE_THRESHOLD` with no critical conflicts are marked eligible for future baseline learning. Exact deliveries receive deterministic fingerprints and are marked duplicates without being silently discarded. Relationship deltas and assumption lifecycle records contribute to conflicts and dashboard evidence. The ML model is cached and safely reloaded when its artifact changes; an invalid replacement leaves the previous valid model active. When no compatible model exists, every forecast explicitly reports `RULE_BASED_FALLBACK` and `ml_model_loaded: false`. Empty forecast requests return `forecast_available: false`, `NO_DATA`, and null probability/confidence rather than fabricated scores.

Attack paths report both `attack_path_risk` and `attack_path_confidence`, and require a directed reachable graph path with supporting evidence. Unsupported stages such as execution, persistence, and privilege escalation are returned as `INSUFFICIENT_EVIDENCE` when network telemetry cannot support them.

## Demonstration mode

Call `/api/network/demo` with `{"scenario":"normal"}` or `{"scenario":"suspicious"}`. The response is labeled `SIMULATED DEMO DATA`; it is safe sample input and is not production telemetry. Submit the returned flow metadata to `/api/network/analyze` to demonstrate feature extraction, baseline comparison, relationship violations, sequence analysis, hybrid forecasting, target ranking, and explanation.
