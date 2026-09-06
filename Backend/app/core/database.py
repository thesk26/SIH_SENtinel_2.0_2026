from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def ensure_schema() -> None:
    inspector = inspect(engine)
    if "network_traffic" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("network_traffic")}
    traffic_additions = {
        "baseline_eligible": "BOOLEAN NOT NULL DEFAULT TRUE",
        "source_event_id": "VARCHAR(128)",
        "event_fingerprint": "VARCHAR(64)",
        "is_duplicate": "BOOLEAN NOT NULL DEFAULT FALSE",
        "ingestion_source": "VARCHAR(30) NOT NULL DEFAULT 'REST'",
    }
    with engine.begin() as connection:
        for name, definition in traffic_additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE network_traffic ADD COLUMN {name} {definition}"))
    forecast_columns = {column["name"] for column in inspector.get_columns("attack_forecasts")} if "attack_forecasts" in inspector.get_table_names() else set()
    additions = {
        "forecast_available": "BOOLEAN NOT NULL DEFAULT TRUE",
        "forecast_source": "VARCHAR(30) NOT NULL DEFAULT 'RULE_BASED_FALLBACK'",
        "ml_probabilities": "JSON",
        "sequence_analysis": "JSON",
        "hybrid_weights": "JSON",
        "evidence": "JSON",
        "ml_confidence_level": "VARCHAR(10) NOT NULL DEFAULT 'LOW'",
        "attack_path": "JSON",
        "attack_stage_probabilities": "JSON",
        "attack_stage_evidence": "JSON",
        "contributing_signals": "JSON",
        "multi_window_analysis": "JSON",
    }
    if forecast_columns:
        with engine.begin() as connection:
            for name, definition in additions.items():
                if name not in forecast_columns:
                    connection.execute(text(f"ALTER TABLE attack_forecasts ADD COLUMN {name} {definition}"))
    if "assumptions" in inspector.get_table_names():
        assumption_columns = {column["name"] for column in inspector.get_columns("assumptions")}
        assumption_additions = {
            "status": "VARCHAR(20) NOT NULL DEFAULT 'CANDIDATE'",
            "supporting_events": "INTEGER NOT NULL DEFAULT 0",
            "contradicting_events": "INTEGER NOT NULL DEFAULT 0",
            "first_verified": "DATETIME",
            "expires_at": "DATETIME",
        }
        with engine.begin() as connection:
            for name, definition in assumption_additions.items():
                if name not in assumption_columns:
                    connection.execute(text(f"ALTER TABLE assumptions ADD COLUMN {name} {definition}"))
    if "assumption_transitions" not in inspector.get_table_names():
        Base.metadata.tables["assumption_transitions"].create(bind=engine, checkfirst=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
