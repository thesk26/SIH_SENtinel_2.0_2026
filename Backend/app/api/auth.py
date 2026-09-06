from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select

from app.core.dependencies import DbSession
from app.core.rate_limit import auth_rate_limit
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RefreshRequest, TokenPair
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["authentication"], dependencies=[Depends(auth_rate_limit)])


@router.post("/register", status_code=status.HTTP_201_CREATED, responses={409: {"description": "Username or email already registered"}})
def register(payload: UserCreate, db: DbSession) -> UserRead:
    existing = db.scalar(select(User).where(or_(User.username == payload.username, User.email == payload.email)))
    if existing:
        raise HTTPException(status_code=409, detail="Username or email is already registered")
    user = User(username=payload.username, email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", responses={401: {"description": "Invalid credentials"}})
def login(payload: LoginRequest, db: DbSession) -> AuthResponse:
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return AuthResponse(access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id), user=user)


@router.post("/refresh", responses={401: {"description": "Invalid refresh token"}})
def refresh(payload: RefreshRequest, db: DbSession) -> TokenPair:
    user_id = decode_token(payload.refresh_token, expected_type="refresh")
    if not user_id or db.get(User, user_id) is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return TokenPair(access_token=create_access_token(user_id), refresh_token=create_refresh_token(user_id))


@router.post("/logout", status_code=204)
def logout() -> None:
    """JWT logout is stateless; clients must discard both tokens."""
    return None
