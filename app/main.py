from fastapi import FastAPI
from app.api.v1 import auth
from app.api.v1 import students, courses, auth, analytics

app = FastAPI(
    title="School Management API",
    description="A modular backend for managing students, courses, and authentication.",
    version="1.0.0"
)
app.include_router(auth.router)

# Include Routers (instead of writing endpoints here)
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to School Management API 🚀"}
