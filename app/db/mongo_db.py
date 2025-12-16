"""
MongoDB connection + collections + sync helpers + ML feeds + Realtime support.
"""

from pymongo import MongoClient, errors
from app.config import settings
import certifi
import logging

# Create module-local logger
logger = logging.getLogger(__name__)


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

        # Dimension & fact collections
        self.dim_students = None
        self.dim_courses = None
        self.dim_lecturers = None
        self.fact_enrollments = None

        # ML + Analytics collections
        self.predictions = None
        self.aggregates = None

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

            # ------------------------------------------------------
            # Initialize collections
            # ------------------------------------------------------
            self.dim_students = self.db.get_collection("dimStudents")
            self.dim_courses = self.db.get_collection("dimCourses")
            self.dim_lecturers = self.db.get_collection("dimLecturers")
            self.fact_enrollments = self.db.get_collection("factEnrollments")

            # ML & Analytics
            self.predictions = self.db.get_collection("predictions")
            self.aggregates = self.db.get_collection("aggregates")

            logger.info(
                "🍃 Mongo collections initialized: "
                "dimStudents, dimCourses, dimLecturers, factEnrollments, "
                "predictions, aggregates"
            )

        except Exception as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            self.client = None
            self.db = None

    # --------------------------------------------------------
    # 🔁 UTILITY: SAFE UPSERT
    # --------------------------------------------------------
    def insert_safe(self, collection, data: dict):
        """Insert or update based on `id`."""
        if not collection or not data:
            return

        key = "id" if "id" in data else "_id"

        try:
            collection.update_one(
                {key: data[key]},
                {"$set": data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"❌ Mongo upsert failed: {e}")

    # --------------------------------------------------------
    # 🔁 BULK INSERTS (for ETL)
    # --------------------------------------------------------
    def bulk_insert(self, collection, data_list: list):
        """Safe bulk insert for analytics and predictions."""
        if not data_list:
            return

        try:
            collection.delete_many({})     # wipe old batch
            collection.insert_many(data_list)
        except Exception as e:
            logger.error(f"❌ Mongo bulk insert failed: {e}")

    # --------------------------------------------------------
    # 🔁 SYNC HELPERS (SQL → Mongo)
    # --------------------------------------------------------
    def sync_student(self, student_dict):
        self.insert_safe(self.dim_students, student_dict)

    def sync_course(self, course_dict):
        self.insert_safe(self.dim_courses, course_dict)

    def sync_lecturer(self, lecturer_dict):
        self.insert_safe(self.dim_lecturers, lecturer_dict)

    def sync_enrollment(self, enr_dict):
        self.insert_safe(self.fact_enrollments, enr_dict)

    # --------------------------------------------------------
    # 🔮 ML SUPPORT
    # --------------------------------------------------------
    def save_prediction(self, pred_dict):
        if not pred_dict:
            return
        try:
            self.predictions.update_one(
                {"StudentID": pred_dict["StudentID"]},
                {"$set": pred_dict},
                upsert=True
            )
        except Exception as e:
            logger.error(f"❌ Failed saving prediction: {e}")

    def save_predictions_batch(self, pred_list):
        self.bulk_insert(self.predictions, pred_list)

    # --------------------------------------------------------
    # 📊 ANALYTICS SUPPORT
    # --------------------------------------------------------
    def save_aggregate(self, doc):
        if not doc:
            return
        try:
            self.aggregates.insert_one(doc)
        except Exception as e:
            logger.error(f"❌ Failed saving aggregate: {e}")

    def replace_aggregates(self, doc_list):
        self.bulk_insert(self.aggregates, doc_list)

    # --------------------------------------------------------
    # ⚡ REALTIME SUPPORT (Change Streams)
    # --------------------------------------------------------
    def watch_changes(self, collection_name):
        try:
            collection = self.db.get_collection(collection_name)
            return collection.watch(full_document='updateLookup')
        except Exception as e:
            logger.error(f"❌ Change stream failed: {e}")
            return None


# --------------------------------------------------------
# 🔥 EXPORT GLOBAL MONGO INSTANCE
# --------------------------------------------------------
mongo_db = MongoDB()
