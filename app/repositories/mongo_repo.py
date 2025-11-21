# app/repositories/mongo_repo.py
from typing import Optional, List, Dict, Any
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from app.db.mongo_db import mongo_db
from app.core.logger import logger


class MongoRepository:
    """Dual-storage Mongo repository used for reads/writes/analytics.

    Assumes `mongo_db` is a valid Database object from pymongo (e.g. client['school_analytics']).
    All collection access is handled through _get_collection() to avoid boolean checks on Collection objects.
    """

    # ----------------------
    # Generic helpers
    # ----------------------
    @staticmethod
    def _clean_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Remove Mongo _id and return copied doc (or None)."""
        if doc is None:
            return None
        # make a shallow copy to avoid mutating original
        cleaned = dict(doc)
        cleaned.pop("_id", None)
        return cleaned

    @staticmethod
    def _clean_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [MongoRepository._clean_doc(d) for d in docs if d is not None]

    @staticmethod
    def _get_collection(name: str) -> Optional[Collection]:
        """Safely get a collection from the mongo_db. Returns None if mongo_db is not configured."""
        try:
            if mongo_db is None:
                logger.warning("mongo_db is None (Mongo not configured)")
                return None
            coll = mongo_db.get_collection(name)
            return coll
        except Exception as exc:
            logger.exception("Error getting collection %s: %s", name, exc)
            return None

    # ----------------------
    # Students
    # ----------------------
    def get_all_students(self) -> List[Dict[str, Any]]:
        coll = self._get_collection("students")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return self._clean_docs(docs)
        except PyMongoError:
            logger.exception("Failed to fetch students")
            return []

    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        coll = self._get_collection("students")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"id": student_id}, {"_id": 0})
            return self._clean_doc(doc)
        except PyMongoError:
            logger.exception("Failed to fetch student by id=%s", student_id)
            return None

    def get_student_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        coll = self._get_collection("students")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"email": email}, {"_id": 0})
            return self._clean_doc(doc)
        except PyMongoError:
            logger.exception("Failed to fetch student by email=%s", email)
            return None

    def upsert_student(self, student_doc: Dict[str, Any]) -> None:
        """Upsert student using 'id' as the key. Logs and returns on failure."""
        coll = self._get_collection("students")
        if coll is None:
            logger.warning("MongoDB not available; skipping upsert_student")
            return
        if "id" not in student_doc:
            logger.error("student_doc missing 'id' field: %s", student_doc)
            return
        try:
            coll.update_one({"id": student_doc["id"]}, {"$set": student_doc}, upsert=True)
        except PyMongoError:
            logger.exception("Failed to upsert student id=%s", student_doc.get("id"))

    def delete_student(self, student_id: int) -> bool:
        coll = self._get_collection("students")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": student_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception("Failed to delete student id=%s", student_id)
            return False

    # ----------------------
    # Courses
    # ----------------------
    def get_all_courses(self) -> List[Dict[str, Any]]:
        coll = self._get_collection("courses")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return self._clean_docs(docs)
        except PyMongoError:
            logger.exception("Failed to fetch courses")
            return []

    def get_course_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        coll = self._get_collection("courses")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"id": course_id}, {"_id": 0})
            return self._clean_doc(doc)
        except PyMongoError:
            logger.exception("Failed to fetch course id=%s", course_id)
            return None

    def upsert_course(self, course_doc: Dict[str, Any]) -> None:
        coll = self._get_collection("courses")
        if coll is None:
            logger.warning("MongoDB not available; skipping upsert_course")
            return
        if "id" not in course_doc:
            logger.error("course_doc missing 'id' field: %s", course_doc)
            return
        try:
            coll.update_one({"id": course_doc["id"]}, {"$set": course_doc}, upsert=True)
        except PyMongoError:
            logger.exception("Failed to upsert course id=%s", course_doc.get("id"))

    def delete_course(self, course_id: int) -> bool:
        coll = self._get_collection("courses")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": course_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception("Failed to delete course id=%s", course_id)
            return False

    # ----------------------
    # Lecturers
    # ----------------------
    def get_all_lecturers(self) -> List[Dict[str, Any]]:
        coll = self._get_collection("lecturers")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return self._clean_docs(docs)
        except PyMongoError:
            logger.exception("Failed to fetch lecturers")
            return []

    def get_lecturer_by_id(self, lecturer_id: int) -> Optional[Dict[str, Any]]:
        coll = self._get_collection("lecturers")
        if coll is None:
            return None
        try:
            doc = coll.find_one({"id": lecturer_id}, {"_id": 0})
            return self._clean_doc(doc)
        except PyMongoError:
            logger.exception("Failed to fetch lecturer id=%s", lecturer_id)
            return None

    def upsert_lecturer(self, lecturer_doc: Dict[str, Any]) -> None:
        coll = self._get_collection("lecturers")
        if coll is None:
            logger.warning("MongoDB not available; skipping upsert_lecturer")
            return
        if "id" not in lecturer_doc:
            logger.error("lecturer_doc missing 'id' field: %s", lecturer_doc)
            return
        try:
            coll.update_one({"id": lecturer_doc["id"]}, {"$set": lecturer_doc}, upsert=True)
        except PyMongoError:
            logger.exception("Failed to upsert lecturer id=%s", lecturer_doc.get("id"))

    def delete_lecturer(self, lecturer_id: int) -> bool:
        coll = self._get_collection("lecturers")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": lecturer_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception("Failed to delete lecturer id=%s", lecturer_id)
            return False

    # ----------------------
    # Enrollments (facts)
    # ----------------------
    def get_all_enrollments(self) -> List[Dict[str, Any]]:
        coll = self._get_collection("enrollments")
        if coll is None:
            return []
        try:
            docs = list(coll.find({}, {"_id": 0}))
            return self._clean_docs(docs)
        except PyMongoError:
            logger.exception("Failed to fetch enrollments")
            return []

    def upsert_enrollment(self, enr_doc: Dict[str, Any]) -> None:
        coll = self._get_collection("enrollments")
        if coll is None:
            logger.warning("MongoDB not available; skipping upsert_enrollment")
            return
        if "id" not in enr_doc:
            logger.error("enr_doc missing 'id' field: %s", enr_doc)
            return
        try:
            coll.update_one({"id": enr_doc["id"]}, {"$set": enr_doc}, upsert=True)
        except PyMongoError:
            logger.exception("Failed to upsert enrollment id=%s", enr_doc.get("id"))

    def delete_enrollment(self, enr_id: int) -> bool:
        coll = self._get_collection("enrollments")
        if coll is None:
            return False
        try:
            res = coll.delete_one({"id": enr_id})
            return res.deleted_count > 0
        except PyMongoError:
            logger.exception("Failed to delete enrollment id=%s", enr_id)
            return False

    # ----------------------
    # Analytics helpers
    # ----------------------
    def gpa_for_student(self, username: str) -> Optional[float]:
        """Compute average 'grade' for given username (or return None)."""
        coll = self._get_collection("enrollments")
        if coll is None:
            return None
        try:
            pipeline = [
                {"$match": {"username": username}},
                {"$group": {"_id": "$username", "avg_gpa": {"$avg": "$grade"}}}
            ]
            results = list(coll.aggregate(pipeline))
            if not results:
                return None
            return float(results[0].get("avg_gpa"))
        except PyMongoError:
            logger.exception("Failed to compute GPA for username=%s", username)
            return None

    def avg_gpa_per_course(self) -> List[Dict[str, Any]]:
        """Return list of dicts: {course_id, avg_gpa, course_title (if available)}"""
        enrollments = self._get_collection("enrollments")
        courses_coll = self._get_collection("courses")
        if enrollments is None:
            return []
        try:
            # Use literal 'courses' as lookup 'from' value (collection name)
            pipeline = [
                {"$group": {"_id": "$course_id", "avg_gpa": {"$avg": "$grade"}}},
                {"$lookup": {
                    "from": courses_coll.name if courses_coll is not None else "courses",
                    "localField": "_id",
                    "foreignField": "id",
                    "as": "course"
                }},
                {"$unwind": {"path": "$course", "preserveNullAndEmptyArrays": True}},
                {"$project": {"course_id": "$_id", "avg_gpa": 1, "course_title": "$course.title"}}
            ]
            results = list(enrollments.aggregate(pipeline))
            # Clean results (remove _id if present)
            cleaned = []
            for r in results:
                r.pop("_id", None)
                cleaned.append(r)
            return cleaned
        except PyMongoError:
            logger.exception("Failed to compute avg_gpa_per_course")
            return []
