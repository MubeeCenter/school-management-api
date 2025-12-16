import logging
import time
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Load DB URL
# ---------------------------------------------------------
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# ---------------------------------------------------------
# Create SQLAlchemy Engine with Proper Pooling
# ---------------------------------------------------------
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite dev-safe
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800
    )
else:
    # Production-grade PostgreSQL / MySQL
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=1800
    )

# ---------------------------------------------------------
# Enable Foreign Keys in SQLite
# ---------------------------------------------------------
@event.listens_for(engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
        logger.info("SQLite foreign_keys enabled")

# ---------------------------------------------------------
# Session Factory
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# Base Class for ORM Models
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# Dependency: Database Session (for FastAPI)
# ---------------------------------------------------------
def get_db():
    """
    FastAPI dependency:
    ✅ One session per request
    ✅ Auto-close after response
    ✅ Safe for concurrency
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# Slow query detection
# ---------------------------------------------------------
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    if total > 0.2:  # threshold: 200ms
        logger.warning(
            "slow_query_detected",
            extra={
                "sql": statement,
                "duration": round(total, 4)
            }
        )
