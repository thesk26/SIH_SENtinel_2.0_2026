import hashlib
from datetime import UTC, datetime


def hash_identifier(value: str | None) -> str | None:
    if not value:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def utc_now() -> datetime:
    """Return a UTC timestamp compatible with the current naive DB columns."""
    return datetime.now(UTC).replace(tzinfo=None)
