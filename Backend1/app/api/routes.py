from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.behavior import router as behavior_router
from app.api.security import router as security_router
from app.api.users import router as users_router
from app.api.network import router as network_router, forecast_router
from app.api.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(behavior_router)
api_router.include_router(security_router)
api_router.include_router(users_router)
api_router.include_router(network_router)
api_router.include_router(forecast_router)
api_router.include_router(dashboard_router)
