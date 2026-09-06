from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    user_id = decode_token(token)
    user = db.get(User, user_id) if user_id else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
