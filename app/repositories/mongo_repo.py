# app/repositories/mongo_repo.py
from app.db.mongo_db import facts_col

class MongoRepository:
    """
    Handles all MongoDB analytics queries.
    """

    @staticmethod
    def average_gpa_per_course():
        """
        Returns average GPA grouped by course name.
        """
        pipeline = [
            {"$group": {"_id": "$CourseName", "avg_gpa": {"$avg": "$GPA"}}},
            {"$project": {"_id": 0, "course": "$_id", "average_gpa": 1}}
        ]
        return list(facts_col.aggregate(pipeline))

    @staticmethod
    def top_students(limit=5):
        """
        Returns top students based on GPA.
        """
        pipeline = [
            {"$sort": {"GPA": -1}},
            {"$limit": limit},
            {"$project": {"_id": 0, "student_name": "$StudentName", "GPA": 1, "CourseName": 1}}
        ]
        return list(facts_col.aggregate(pipeline))

    @staticmethod
    def course_enrollment_count():
        """
        Counts how many students enrolled in each course.
        """
        pipeline = [
            {"$group": {"_id": "$CourseName", "total_students": {"$sum": 1}}},
            {"$project": {"_id": 0, "course": "$_id", "total_students": 1}}
        ]
        return list(facts_col.aggregate(pipeline))

def gpa_for_student(self, username):
    record = self.db["factEnrollments"].aggregate([
        {"$match": {"StudentEmail": username}},
        {"$group": {"_id": "$StudentEmail", "avg_gpa": {"$avg": "$GPA"}}}
    ])
    for r in record:
        return r["avg_gpa"]
    return None
