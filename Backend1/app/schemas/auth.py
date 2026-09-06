from pydantic import BaseModel, Field

from app.schemas.user import UserRead


class LoginRequest(BaseModel):
    username: str
    password: str = Field(min_length=1)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthResponse(TokenPair):
    user: UserRead
