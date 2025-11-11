from fastapi import FastAPI
from app.db.sql_db import Base, engine

# ⚠️ Import all models explicitly so metadata knows them
from app.models.sqlalchemy_models import (
    UserModel,
    Course,
    Student,
    Lecturer,
    Enrollment,
    # include every SQLAlchemy model class you defined
)

# from app.db.mongo_db import mongo_client  # temporarily disabled (Mongo not yet implemented)

from app.api.v1 import auth, students, courses, analytics

app = FastAPI(
    title="School Management API",
    description="A modular backend for managing students, courses, and authentication.",
    version="1.0.0"
)

@app.on_event("startup")
def create_tables():
    print("🔧 Creating tables if missing…")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables ready!")

# Include routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to School Management API 🚀"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
