from app.api.auth import router as auth_router
from app.api.behavior import router as behavior_router
from app.api.network import forecast_router, router as network_router
from app.api.security import router as security_router
from app.api.users import router as users_router
from app.api.dashboard import router as dashboard_router
from app.api.devices import router as devices_router
from app.api.response import router as response_router
from app.api.collector import public_router as public_collector_router, router as collector_router
from app.core.config import settings
from app.core.database import Base, engine, ensure_schema
from app import models  # noqa: F401
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.ml_forecasting_service import model_status
from sqlalchemy import text

Base.metadata.create_all(bind=engine)
ensure_schema()

app = FastAPI(
    title=settings.app_name,
    description="Assumption Integrity-based continuous security API.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
for router in (auth_router, behavior_router, security_router, users_router, network_router, forecast_router, dashboard_router, devices_router, response_router, collector_router, public_collector_router):
    app.include_router(router, prefix="/api")


@app.get("/health", tags=["health"])
def health() -> dict:
    database_status = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "unavailable"
    model = model_status()
    return {"status": "ok" if database_status == "ok" else "degraded", "service": settings.app_name, "database": database_status, "ml_model_loaded": model["loaded"], "model_version": model["version"] or "none"}


@app.get("/system/health", tags=["health"])
def system_health() -> dict:
    return health()
