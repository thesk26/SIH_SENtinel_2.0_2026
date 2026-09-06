from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    payload = {"sub": subject, "type": token_type, "exp": datetime.now(UTC) + expires_delta}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def create_access_token(subject: str) -> str:
    return create_token(subject, "access", timedelta(minutes=settings.access_token_expire_minutes))


def create_refresh_token(subject: str) -> str:
    return create_token(subject, "refresh", timedelta(days=settings.refresh_token_expire_days))


def decode_token(token: str, expected_type: str = "access") -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type or not payload.get("sub"):
            return None
        return str(payload["sub"])
    except JWTError:
        return None
