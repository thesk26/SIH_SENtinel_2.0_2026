from collections import defaultdict
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    """Development fallback; replace with RedisRateLimiter for multi-worker deployments."""

    def __init__(self) -> None:
        self._entries: dict[str, tuple[float, int]] = defaultdict(lambda: (0.0, 0))
        self._lock = Lock()

    def allow(self, key: str, limit: int, window_seconds: int = 60) -> bool:
        now = monotonic()
        with self._lock:
            started, count = self._entries[key]
            if now - started >= window_seconds:
                self._entries[key] = (now, 1)
                return True
            if count >= limit:
                return False
            self._entries[key] = (started, count + 1)
            return True


class RedisRateLimiter:
    """Redis adapter contract for deployments with multiple API workers."""

    def __init__(self, redis_client: object) -> None:
        self.redis = redis_client

    def allow(self, key: str, limit: int, window_seconds: int = 60) -> bool:
        bucket = f"sentinal:rate:{key}"
        count = self.redis.incr(bucket)
        if count == 1:
            self.redis.expire(bucket, window_seconds)
        return count <= limit


limiter = InMemoryRateLimiter()


def enforce_rate_limit(request: Request, namespace: str, limit: int) -> None:
    client_host = request.client.host if request.client else "unknown"
    key = f"{namespace}:{client_host}"
    if not limiter.allow(key, limit):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")


def auth_rate_limit(request: Request) -> None:
    enforce_rate_limit(request, "auth", 30)


def security_rate_limit(request: Request) -> None:
    enforce_rate_limit(request, "security", 120)
