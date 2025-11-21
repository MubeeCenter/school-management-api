"""
MongoDB connection + collections + sync helpers.
"""

from pymongo import MongoClient, errors
from app.config import settings
from app.core.logger import logger
import certifi


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

        # Collections
        self.students = None
        self.courses = None
        self.lecturers = None
        self.enrollments = None  # factEnrollments

        self.connect()

    # --------------------------------------------------------
    # 🔌 CONNECT TO MONGODB
    # --------------------------------------------------------
    def connect(self):
        uri = settings.MONGO_URI

        if not uri:
            logger.warning("⚠ MongoDB URI not set. Running in SQL-only mode.")
            return

        try:
            self.client = MongoClient(
                uri,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=7000,
                retryWrites=True,
            )

            # Test connection
            self.client.admin.command("ping")
            logger.info("🍃 MongoDB connection successful.")

            # Select DB
            self.db = self.client[settings.MONGO_DB_NAME]

            # Initialize collections safely
            self.students = self.db.get_collection(settings.MONGO_COLLECTION_STUDENTS)
            self.courses = self.db.get_collection(settings.MONGO_COLLECTION_COURSES)
            self.lecturers = self.db.get_collection(settings.MONGO_COLLECTION_LECTURERS)
            self.enrollments = self.db.get_collection(settings.MONGO_COLLECTION_FACTS)

            logger.info(
                f"🍃 MongoDB collections initialized: "
                f"{settings.MONGO_COLLECTION_STUDENTS}, "
                f"{settings.MONGO_COLLECTION_COURSES}, "
                f"{settings.MONGO_COLLECTION_LECTURERS}, "
                f"{settings.MONGO_COLLECTION_FACTS}"
            )

        except Exception as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            self.client = None
            self.db = None

    # --------------------------------------------------------
    # 🔁 UTILITY: SAFE UPSERT
    # --------------------------------------------------------
    def insert_safe(self, collection, data: dict):
        """
        Insert or update document based on `id`.
        This prevents duplicates and keeps data up-to-date.
        """
        if not collection or not data:
            return

        if "id" not in data:
            logger.warning("⚠ insert_safe called without 'id'. Skipping.")
            return

        try:
            collection.update_one(
                {"id": data["id"]},
                {"$set": data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"❌ Mongo upsert failed: {e}")

    # --------------------------------------------------------
    # 🔁 SYNC HELPERS (SQL → Mongo)
    # --------------------------------------------------------
    def sync_course(self, course_dict):
        """Sync a course from SQL to Mongo."""
        self.insert_safe(self.courses, course_dict)

    def sync_student(self, student_dict):
        """Sync a student from SQL to Mongo."""
        self.insert_safe(self.students, student_dict)

    def sync_lecturer(self, lecturer_dict):
        """Sync a lecturer from SQL to Mongo."""
        self.insert_safe(self.lecturers, lecturer_dict)

    def sync_enrollment(self, enr_dict):
        """
        Sync an enrollment record (Fact table).
        This is what analytics uses.
        """
        self.insert_safe(self.enrollments, enr_dict)


# --------------------------------------------------------
# 🔥 EXPORT GLOBAL MONGO INSTANCE
# --------------------------------------------------------
mongo_db = MongoDB()
