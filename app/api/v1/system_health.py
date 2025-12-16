from fastapi import APIRouter
from sqlalchemy import text
from app.db.sql_db import engine
import redis
from pymongo import MongoClient
import psutil

router = APIRouter(prefix="/health", tags=["Health Checks"])

# -------------------------------------------------------
# 1️⃣ Liveness Probe
# -------------------------------------------------------
@router.get("/live")
def live():
    return {"status": "alive"}


# -------------------------------------------------------
# 2️⃣ Readiness Probe
# -------------------------------------------------------
@router.get("/ready")
def ready():
    issues = []

    # SQL check
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        issues.append(f"SQL error: {str(e)}")

    # Redis check
    try:
        r = redis.Redis(host="redis", port=6379)
        r.ping()
    except Exception as e:
        issues.append(f"Redis error: {str(e)}")

    # MongoDB check
    try:
        mongo = MongoClient("mongodb://mongo:27017", serverSelectionTimeoutMS=200)
        mongo.admin.command("ping")
    except Exception as e:
        issues.append(f"MongoDB error: {str(e)}")

    return {
        "ready": len(issues) == 0,
        "issues": issues,
        "services": ["sql", "redis", "mongo"]
    }


# -------------------------------------------------------
# 3️⃣ Deep Health (Full System Diagnostic)
# -------------------------------------------------------
@router.get("/deep")
def deep_health():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return {
        "status": "OK",
        "system": {
            "cpu_usage": cpu,
            "memory_usage": mem,
            "disk_usage": disk
        }
    }
