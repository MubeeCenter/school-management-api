# app/repositories/mongo_repo.py

from typing import Optional, List, Dict, Any
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from app.db.mongo_db import mongo_db
import logging  # ✅ Use module-local logger

# Module-level logger
logger = logging.getLogger(__name__)


class MongoRepository:
    """
    Mongo repository with safe fallback when MongoDB is disabled.
    """

    # -------------------------
    # Helpers
    # -------------------------

    @staticmethod
    def _clean_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if doc is None:
            return None
        cleaned = dict(doc)
        cleaned.pop("_id", None)
        return cleaned

    @staticmethod
    def _clean_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [MongoRepository._clean_doc(d) for d in docs if d]

    @staticmethod
    def _get_collection(name: str) -> Optional[Collection]:
        """Return a MongoDB collection, or None if connection unavailable."""
        try:
            if mongo_db.db is None:
                logger.warning("MongoDB not available. Returning None for collection.")
                return None
            return mongo_db.db.get_collection(name)
        except Exception as exc:
            logger.exception(f"Failed to get collection '{name}': {exc}")
            return None

    # -------------------------
    # STUDENTS
    # -------------------------

    def get_all_students(self) -> List[Dict[str, Any]]:
        coll = self._get_collection("students")
        if coll is None:
            return []
        try:
            return list(coll.find({}, {"_id": 0}))
        except PyMongoError:
            logger.exception("Failed to fetch students")
            return []

    def get_student_by_id(self, student_id: int):
        coll = self._get_collection("students")
        if coll is None:
            return None
        try:
            return coll.find_one({"id": student_id}, {"_id": 0})
        except PyMongoError:
            logger.exception(f"Failed to fetch student id={student_id}")
            return None

    def get_student_by_email(self, email: str):
        coll = self._get_collection("students")
        if coll is None:
            return None
        try:
            return coll.find_one({"email": email}, {"_id": 0})
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

    # -------------------------
    # COURSES
    # -------------------------
    # (rest of your methods remain the same)
