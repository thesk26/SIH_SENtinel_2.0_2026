from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SENTINAL"
    environment: str = "development"
    secret_key: str = Field("development-secret-change-me", min_length=16)
    database_url: str = "sqlite:///./sentinal.db"
    redis_url: str = "redis://localhost:6379/0"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    baseline_days: int = 15
    pass_threshold: float = 80.0
    challenge_threshold: float = 50.0
    baseline_update_threshold: float = 80.0
    ml_model_path: str = "app/ml/models/network_forecast.pkl"
    ml_forecast_weight: float = Field(0.40, ge=0, le=1)
    sequence_analysis_weight: float = Field(0.25, ge=0, le=1)
    relationship_analysis_weight: float = Field(0.20, ge=0, le=1)
    integrity_analysis_weight: float = Field(0.15, ge=0, le=1)
    max_predicted_targets: int = Field(3, ge=1, le=20)
    default_analysis_window_minutes: int = Field(15, ge=1, le=1440)
    short_window_minutes: int = Field(5, ge=1, le=1440)
    medium_window_minutes: int = Field(30, ge=1, le=1440)
    long_window_minutes: int = Field(60, ge=1, le=1440)
    high_confidence_threshold: float = Field(0.80, ge=0, le=1)
    medium_confidence_threshold: float = Field(0.60, ge=0, le=1)
    low_confidence_threshold: float = Field(0.40, ge=0, le=1)
    model_version: str = "1.0.0"
    preprocessing_version: str = "1.0.0"
    assumption_candidate_events: int = Field(2, ge=1)
    assumption_learning_events: int = Field(3, ge=2)
    assumption_trust_events: int = Field(5, ge=3)
    assumption_trust_confidence: float = Field(0.8, ge=0, le=1)
    assumption_expiry_days: int = Field(30, ge=1)
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]
    collector_stale_seconds: int = Field(90, ge=10)

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


settings = Settings()
