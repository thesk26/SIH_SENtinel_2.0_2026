from fastapi import APIRouter

from app.core.dependencies import CurrentUser
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(current_user: CurrentUser) -> UserRead:
    return current_user
