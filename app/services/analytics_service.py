# app/services/analytics_service.py
from app.repositories.mongo_repo import MongoRepository

class AnalyticsService:
    """
    Business logic for school analytics.
    """

    def __init__(self):
        self.repo = MongoRepository()

    def get_average_gpa(self):
        """
        Fetches average GPA per course.
        """
        results = self.repo.average_gpa_per_course()
        if not results:
            return {"message": "No GPA records found"}
        return results

    def get_top_students(self, limit=5):
        """
        Returns the top N students by GPA.
        """
        return self.repo.top_students(limit)

    def get_course_enrollments(self):
        """
        Returns course enrollment summary.
        """
        return self.repo.course_enrollment_count()
