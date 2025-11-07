# app/api/v1/analytics.py
from fastapi import APIRouter, Query
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

analytics_service = AnalyticsService()

@router.get("/gpa", summary="Average GPA per course")
def average_gpa():
    """
    Returns average GPA per course from MongoDB.
    """
    return analytics_service.get_average_gpa()


@router.get("/top-students", summary="Top students by GPA")
def top_students(limit: int = Query(5, ge=1, le=50)):
    """
    Returns the top students based on GPA.
    """
    return analytics_service.get_top_students(limit)


@router.get("/enrollments", summary="Course enrollment count")
def course_enrollments():
    """
    Returns how many students enrolled in each course.
    """
    return analytics_service.get_course_enrollments()
