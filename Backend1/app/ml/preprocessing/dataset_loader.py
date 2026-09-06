from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any


def normalize_column_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


def load_csv_dataset(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Dataset file does not exist: {path}")
    try:
        with path.open(newline="", encoding="utf-8-sig") as dataset_file:
            reader = csv.DictReader(dataset_file)
            if not reader.fieldnames:
                raise ValueError("Dataset must contain a CSV header row")
            headers = [normalize_column_name(value) for value in reader.fieldnames]
            if len(headers) != len(set(headers)):
                raise ValueError("Dataset contains duplicate column names after normalization")
            rows = []
            for raw_row in reader:
                row = {normalize_column_name(key): (value.strip() if isinstance(value, str) else value) for key, value in raw_row.items()}
                rows.append(row)
    except UnicodeDecodeError as error:
        raise ValueError("Dataset must be a UTF-8 CSV file") from error
    except csv.Error as error:
        raise ValueError(f"Dataset CSV is invalid: {error}") from error
    if not rows:
        raise ValueError("Dataset is empty")
    return rows, headers
