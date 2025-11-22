# app/repositories/mongo_repo.py

from typing import Optional, List, Dict, Any
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from app.db.mongo_db import mongo_db
from app.core.logger import logger


class MongoRepository:
    """
    Dual-storage Mongo repository used for reads/writes/analytics.
    All collection access is handled through _get_collection() to avoid errors when Mongo is disabled.
    """

    # --------------------------------------------------------
    # Generic cleaning helpers (remove _id)
    # --------------------------------------------------------
    @staticmethod
    def _clean_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if doc is None:
            return None
        cleaned = dict(doc)
        cleaned.pop("_id", None)
        return cleaned

    @staticmethod
    def _clean_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [MongoRepository._clean_doc(d) for d in docs if d is not None]

    @staticmethod
    def _get_collection(name: str) -> Optional[Collection]:
        """
        Safely get a collection from MongoDB.
        Returns None if Mongo is disabled or connection failed.
        """
        try:
            if mongo_db.db is None:
                logger.warning("MongoDB disabled or not connected.")
                return None
            return mongo_db.db.get_collection(name)
        except Exception as exc:
            logger.exception(f"Failed to get Mongo collection '{name}': {exc}")
            return None

    # --------------------------------------------------------
    # Students
    # --------------------------------------------------------
    def get_all_students(self) -> List[Dict[str, Any]]:
        coll = self._get_collection("students")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return docs
        except PyMongoError:
            logger.exception("Failed to fetch students")
            return []

    def get_student_by_id(self, student_id: int):
        coll = self._get_collection("students")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"id": student_id}, {"_id": 0})
            return doc
        except PyMongoError:
            logger.exception(f"Failed to fetch student id={student_id}")
            return None

    def get_student_by_email(self, email: str):
        coll = self._get_collection("students")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"email": email}, {"_id": 0})
            return doc
        except PyMongoError:
            logger.exception(f"Failed to fetch student email={email}")
            return None

    def upsert_student(self, doc: Dict[str, Any]):
        coll = self._get_collection("students")
        if coll is None:
            return
        try:
            coll.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
        except PyMongoError:
            logger.exception(f"Failed to upsert student id={doc.get('id')}")

    def delete_student(self, student_id: int) -> bool:
        coll = self._get_collection("students")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": student_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception(f"Failed to delete student id={student_id}")
            return False

    # --------------------------------------------------------
    # Courses
    # --------------------------------------------------------
    def get_all_courses(self):
        coll = self._get_collection("courses")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return docs
        except PyMongoError:
            logger.exception("Failed to fetch courses")
            return []

    def get_course_by_id(self, course_id: int):
        coll = self._get_collection("courses")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"id": course_id}, {"_id": 0})
            return doc
        except PyMongoError:
            logger.exception(f"Failed to fetch course id={course_id}")
            return None

    def upsert_course(self, doc: Dict[str, Any]):
        coll = self._get_collection("courses")
        if coll is None:
            return
        try:
            coll.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
        except PyMongoError:
            logger.exception(f"Failed to upsert course id={doc.get('id')}")

    def delete_course(self, course_id: int) -> bool:
        coll = self._get_collection("courses")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": course_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception(f"Failed to delete course id={course_id}")
            return False

    # --------------------------------------------------------
    # Lecturers
    # --------------------------------------------------------
    def get_all_lecturers(self):
        coll = self._get_collection("lecturers")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return docs
        except PyMongoError:
            logger.exception("Failed to fetch lecturers")
            return []

    def get_lecturer_by_id(self, lecturer_id: int):
        coll = self._get_collection("lecturers")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"id": lecturer_id}, {"_id": 0})
            return doc
        except PyMongoError:
            logger.exception(f"Failed to fetch lecturer id={lecturer_id}")
            return None

    def upsert_lecturer(self, doc: Dict[str, Any]):
        coll = self._get_collection("lecturers")
        if coll is None:
            return
        try:
            coll.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
        except PyMongoError:
            logger.exception(f"Failed to upsert lecturer id={doc.get('id')}")

    def delete_lecturer(self, lecturer_id: int) -> bool:
        coll = self._get_collection("lecturers")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": lecturer_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception(f"Failed to delete lecturer id={lecturer_id}")
            return False

    # --------------------------------------------------------
    # Enrollments (FACT table)
    # --------------------------------------------------------
    def get_all_enrollments(self):
        coll = self._get_collection("enrollments")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return docs
        except PyMongoError:
            logger.exception("Failed to fetch enrollments")
            return []

    def upsert_enrollment(self, doc: Dict[str, Any]):
        coll = self._get_collection("enrollments")
        if coll is None:
            return
        try:
            coll.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
        except PyMongoError:
            logger.exception(f"Failed to upsert enrollment id={doc.get('id')}")

    def delete_enrollment(self, enr_id: int) -> bool:
        coll = self._get_collection("enrollments")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": enr_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception(f"Failed to delete enrollment id={enr_id}")
            return False

    # --------------------------------------------------------
    # ANALYTICS FUNCTIONS (NEW + COMPLETE)
    # --------------------------------------------------------

    def top_students(self, limit: int = 5):
        """Return top N students by GPA."""
        enr = self._get_collection("enrollments")
        students = self._get_collection("students")
        if enr is None:
            return []

        try:
            pipeline = [
                {"$group": {"_id": "$student_id", "gpa": {"$avg": "$grade"}}},
                {"$sort": {"gpa": -1}},
                {"$limit": limit},
                {"$lookup": {
                    "from": students.name if students else "students",
                    "localField": "_id",
                    "foreignField": "id",
                    "as": "student"
                }},
                {"$unwind": "$student"},
                {"$project": {
                    "_id": 0,
                    "student_id": "$_id",
                    "name": "$student.name",
                    "email": "$student.email",
                    "gpa": 1
                }}
            ]
            return list(enr.aggregate(pipeline))

        except Exception as e:
            logger.exception(f"Failed to compute top_students: {e}")
            return []

    def course_enrollment_count(self):
        """Return enrollment count per course."""
        enr = self._get_collection("enrollments")
        courses = self._get_collection("courses")
        if enr is None:
            return []

        try:
            pipeline = [
                {"$group": {"_id": "$course_id", "enrollment_count": {"$sum": 1}}},
                {"$lookup": {
                    "from": courses.name if courses else "courses",
                    "localField": "_id",
                    "foreignField": "id",
                    "as": "course"
                }},
                {"$unwind": "$course"},
                {"$project": {
                    "_id": 0,
                    "course_id": "$_id",
                    "course_name": "$course.title",
                    "course_code": "$course.code",
                    "enrollment_count": 1
                }}
            ]
            return list(enr.aggregate(pipeline))

        except Exception as e:
            logger.exception(f"Failed to compute course_enrollment_count: {e}")
            return []

    def gpa_by_course(self):
        """Return GPA analytics for each course."""
        enr = self._get_collection("enrollments")
        courses = self._get_collection("courses")
        if enr is None:
            return []

        try:
            pipeline = [
                {"$group": {
                    "_id": "$course_id",
                    "avg_gpa": {"$avg": "$grade"},
                    "count": {"$sum": 1}
                }},
                {"$lookup": {
                    "from": courses.name if courses else "courses",
                    "localField": "_id",
                    "foreignField": "id",
                    "as": "course"
                }},
                {"$unwind": {"path": "$course", "preserveNullAndEmptyArrays": True}},
                {"$project": {
                    "_id": 0,
                    "course_id": "$_id",
                    "course_name": "$course.title",
                    "course_code": "$course.code",
                    "avg_gpa": 1,
                    "count": 1
                }}
            ]

            return list(enr.aggregate(pipeline))
        except Exception as e:
            logger.exception(f"Failed to compute gpa_by_course: {e}")
            return []
