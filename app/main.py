from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from app.db.sql_db import Base, engine
from app.db.mongo_db import mongo_client  # if you have MongoDB connection setup

# ✅ Import all models explicitly so SQLAlchemy knows them
from app.models.sqlalchemy_models import (
    UserModel,
    Course,
    Student,
    Lecturer,
    Enrollment,
)

# ✅ Import routers
from app.api.v1 import auth, students, courses, analytics

# ✅ Initialize app
app = FastAPI(
    title="School Management API",
    description="A modular backend for managing students, courses, lecturers, and analytics.",
    version="1.0.0",
)

# ✅ Startup event — safe table creation + MongoDB connection
@app.on_event("startup")
def startup_event():
    # Connect to MongoDB
    try:
        mongo_client.admin.command("ping")
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")

    # Safe SQLite table creation
    try:
        print("🔧 Creating tables if missing…")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables ready!")
    except OperationalError as e:
        if "already exists" in str(e):
            print("⚠️ Tables already exist, skipping creation.")
        else:
            raise

# ✅ Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    try:
        mongo_client.close()
        print("🧹 MongoDB connection closed.")
    except Exception:
        pass

# ✅ Include all routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(analytics.router)

# ✅ Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the School Management API 🚀"}
