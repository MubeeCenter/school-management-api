from app.repositories.mongo_repo import MongoRepository
from app.core.async_cache import get_cache, set_cache


class AnalyticsService:
    """
    Business logic for school analytics (MongoDB + Redis Cache).
    """

    def __init__(self):
        self.repo = MongoRepository()

    async def get_average_gpa(self):
        """
        Fetch average GPA per course (CACHED).
        """
        cache_key = "avg_gpa_v1"

        cached = await get_cache(cache_key)
        if cached:
            return {"source": "redis", "data": cached}

        results = self.repo.gpa_by_course()

        if not results:
            return {"message": "No GPA records found"}

        await set_cache(cache_key, results, ttl=300)
        return {"source": "database", "data": results}

    async def get_top_students(self, limit: int = 5):
        """
        Returns the top N students by GPA (CACHED).
        """
        cache_key = f"top_students_{limit}_v1"

        cached = await get_cache(cache_key)
        if cached:
            return {"source": "redis", "data": cached}

        results = self.repo.top_students(limit)

        await set_cache(cache_key, results, ttl=300)
        return {"source": "database", "data": results}

    async def get_course_enrollments(self):
        """
        Returns course enrollment summary (CACHED).
        """
        cache_key = "course_enrollments_v1"

        cached = await get_cache(cache_key)
        if cached:
            return {"source": "redis", "data": cached}

        results = self.repo.course_enrollment_count()

        await set_cache(cache_key, results, ttl=300)
        return {"source": "database", "data": results}
