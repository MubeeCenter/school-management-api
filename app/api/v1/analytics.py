from fastapi import APIRouter, Query
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

analytics_service = AnalyticsService()


@router.get("/gpa", summary="Average GPA per course")
async def average_gpa():
    """
    Returns average GPA per course from MongoDB (Cached with Redis).
    """
    return await analytics_service.get_average_gpa()


@router.get("/top-students", summary="Top students by GPA")
async def top_students(limit: int = Query(5, ge=1, le=50)):
    """
    Returns the top students based on GPA (Cached with Redis).
    """
    return await analytics_service.get_top_students(limit)


@router.get("/enrollments", summary="Course enrollment count")
async def course_enrollments():
    """
    Returns how many students enrolled in each course (Cached with Redis).
    """
    return await analytics_service.get_course_enrollments()
