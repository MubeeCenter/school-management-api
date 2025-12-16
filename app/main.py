from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import inspect
import time
import logging
import redis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.config import settings
from app.core.logger import setup_logging
from app.core.error_handler import add_exception_handlers
from app.core.security import hash_password
from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

from app.db.sql_db import Base, engine, SessionLocal
from app.models.sqlalchemy_models import (
    UserModel,
    Course,
    Student,
    Lecturer,
    Enrollment,
)
# --------------------------------------------------------
# 🔧 Logging (INITIALIZE ONCE)
# --------------------------------------------------------
setup_logging()
logger = logging.getLogger(__name__)

# --------------------------------------------------------
# 🚀 FastAPI App
# --------------------------------------------------------
app = FastAPI(
    title="School Management API",
    description=(
        "A modular backend for managing students, lecturers, courses, "
        "and analytics with authentication, ML predictions, "
        "real-time dashboards, and automated reporting."
    ),
    version="3.1.0",
    docs_url=None,
    redoc_url=None
)

# Register Global Exception Handlers
add_exception_handlers(app)

# --------------------------------------------------------
# 🌐 CORS Configuration
# --------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------
# 🔥 RAW Request Body Logger (DEBUG ONLY)
# --------------------------------------------------------
@app.middleware("http")
async def log_request_body(request: Request, call_next):
    body = await request.body()

    if body:
        logger.debug(
            "raw_request_body",
            extra={
                "method": request.method,
                "path": request.url.path,
                "size": len(body),
            },
        )

    response = await call_next(request)
    return response
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
# --------------------------------------------------------
# ⏱️ PERFORMANCE TIMING MIDDLEWARE
# --------------------------------------------------------
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    logger.info(
        "request_timing",
        extra={
            "method": request.method,
            "path": request.url.path,
            "duration_ms": round(duration * 1000, 2),
        },
    )

    return response

# --------------------------------------------------------
# 📊 PROMETHEUS METRICS MIDDLEWARE
# --------------------------------------------------------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)

    REQUEST_COUNT.labels(
        method,
        endpoint,
        response.status_code,
    ).inc()

    return response

# --------------------------------------------------------
# 🗄️ Database Startup Event — Create Tables
# --------------------------------------------------------
@app.on_event("startup")
def create_tables():
    logger.info("checking_existing_tables")
    inspector = inspect(engine)

    try:
        existing_tables = inspector.get_table_names()
        if existing_tables:
            logger.info(
                "existing_tables_found",
                extra={"tables": existing_tables},
            )
        else:
            logger.warning("no_tables_found_creating_schema")
            Base.metadata.create_all(bind=engine)
            logger.info("tables_created_successfully")
    except Exception as e:
        logger.warning(
            "table_creation_skipped",
            extra={"error": str(e)},
        )

# --------------------------------------------------------
# 🔐 Auto-Create Default Admin
# --------------------------------------------------------
@app.on_event("startup")
def create_default_admin():
    db = SessionLocal()
    try:
        logger.info("checking_default_admin")

        admin = db.query(UserModel).filter_by(username="admin").first()
        if not admin:
            logger.warning("creating_default_admin")

            admin = UserModel(
                username="admin",
                password=hash_password("Admin123"),
                role="admin",
            )
            db.add(admin)
            db.commit()

            logger.info("default_admin_created")
        else:
            logger.info("admin_already_exists")

    except Exception as e:
        logger.error(
            "admin_creation_failed",
            extra={"error": str(e)},
        )
    finally:
        db.close()

# --------------------------------------------------------
# ⚡ Redis Cache Health Check
# --------------------------------------------------------
@app.on_event("startup")
def check_redis_connection():
    try:
        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
        )
        r.ping()
        logger.info("redis_connected")
    except Exception as e:
        logger.warning(
            "redis_unavailable",
            extra={"error": str(e)},
        )

# --------------------------------------------------------
# 🔗 Include Routers
# --------------------------------------------------------
from app.api.v1 import (
    auth,
    students,
    courses,
    lecturers,
    analytics,
    grades,
    ml,
    realtime,
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(lecturers.router)
app.include_router(analytics.router)
app.include_router(grades.router)
app.include_router(ml.router)
app.include_router(realtime.router)

# --------------------------------------------------------
# 🌍 Public Routes
# --------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to School Management API 🚀"}

@app.get("/healthz", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "school-management-api"}

# --------------------------------------------------------
# 📈 Prometheus Metrics Endpoint
# --------------------------------------------------------
@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://school-frontend.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
