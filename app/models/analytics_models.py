# app/models/analytics_models.py

from pydantic import BaseModel


class GPAAnalytics(BaseModel):
    course_name: str
    course_code: str
    avg_gpa: float
    count: int


class TopStudentAnalytics(BaseModel):
    name: str
    email: str
    gpa: float


class EnrollmentAnalytics(BaseModel):
    course_name: str
    course_code: str
    enrollment_count: int
