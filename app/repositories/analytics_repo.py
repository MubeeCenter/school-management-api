# app/repositories/analytics_repo.py

from app.db.mongo_db import (
    students_col,
    courses_col,
    lecturers_col,
    facts_col
)


class AnalyticsRepository:

    # 📌 1. Average GPA per course
    def get_average_gpa(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$course_id",
                    "avg_gpa": {"$avg": "$grade"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$lookup": {
                    "from": courses_col.name,
                    "localField": "_id",
                    "foreignField": "sql_id",
                    "as": "course"
                }
            },
            {"$unwind": "$course"},
            {
                "$project": {
                    "course_name": "$course.title",
                    "course_code": "$course.code",
                    "avg_gpa": 1,
                    "count": 1
                }
            }
        ]

        return list(facts_col.aggregate(pipeline))

    # 📌 2. Top Students by GPA
    def get_top_students(self, limit: int = 5):
        pipeline = [
            {
                "$group": {
                    "_id": "$student_id",
                    "gpa": {"$avg": "$grade"}
                }
            },
            {
                "$lookup": {
                    "from": students_col.name,
                    "localField": "_id",
                    "foreignField": "sql_id",
                    "as": "student"
                }
            },
            {"$unwind": "$student"},
            {"$sort": {"gpa": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "name": "$student.name",
                    "email": "$student.email",
                    "gpa": 1
                }
            }
        ]

        return list(facts_col.aggregate(pipeline))

    # 📌 3. Course Enrollment Count
    def get_course_enrollments(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$course_id",
                    "enrollment_count": {"$sum": 1}
                }
            },
            {
                "$lookup": {
                    "from": courses_col.name,
                    "localField": "_id",
                    "foreignField": "sql_id",
                    "as": "course"
                }
            },
            {"$unwind": "$course"},
            {
                "$project": {
                    "course_name": "$course.title",
                    "course_code": "$course.code",
                    "enrollment_count": 1
                }
            }
        ]

        return list(facts_col.aggregate(pipeline))
