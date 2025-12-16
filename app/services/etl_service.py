# app/services/etl_service.py

"""
Internal ETL Service (SQL → MongoDB)
------------------------------------

Purpose:
✔ Sync SQL database (Students, Courses, Enrollments) to MongoDB fact tables.
✔ Lightweight and fast for API-triggered updates.
✔ Works together with scripts/etl_sync.py (CSV ETL).

Used by:
- /etl/run API endpoint
- Internal automation (after grade updates)
- Machine learning pipelines
"""

import logging
import pandas as pd
from app.db.sql_db import SessionLocal
from app.db.mongo_db import facts_col
from app.models.sqlalchemy_models import Enrollment, Student, Course, Lecturer

# Module-level logger
logger = logging.getLogger(__name__)


class ETLService:

    def extract(self) -> pd.DataFrame:
        """
        Extract data from SQL database (JOIN Students, Enrollments, Courses, Lecturers)
        """
        db = SessionLocal()
        try:
            query = (
                db.query(
                    Enrollment,
                    Student,
                    Course,
                    Lecturer
                )
                .join(Student, Enrollment.student_id == Student.id)
                .join(Course, Enrollment.course_id == Course.id)
                .join(Lecturer, Course.lecturer_id == Lecturer.id)
            )

            rows = []
            for e, s, c, l in query:
                rows.append({
                    "StudentID": s.id,
                    "StudentName": s.name,
                    "CourseID": c.id,
                    "CourseName": c.course_name,
                    "Lecturer": l.name,
                    "Grade": e.grade,
                    "GPA": e.gpa,
                    "Semester": c.semester
                })

            logger.info("ETL extract completed", extra={"rows": len(rows)})
            return pd.DataFrame(rows)
        except Exception as e:
            logger.exception(f"ETL extraction failed: {e}")
            return pd.DataFrame()
        finally:
            db.close()

    def load_to_mongo(self, df: pd.DataFrame, clean=False):
        """
        Load extracted data to MongoDB.
        """
        if clean:
            facts_col.delete_many({})
            logger.info("MongoDB facts collection cleared before load")

        if not df.empty:
            try:
                facts_col.insert_many(df.to_dict("records"))
                logger.info("ETL load completed", extra={"rows": len(df)})
            except Exception as e:
                logger.exception(f"ETL load to MongoDB failed: {e}")
        else:
            logger.warning("ETL load skipped: no data to insert")

    def run_full(self, clean=False):
        """
        Full ETL pipeline.
        """
        logger.info("ETL pipeline started", extra={"clean": clean})
        df = self.extract()
        self.load_to_mongo(df, clean=clean)
        logger.info("ETL pipeline finished", extra={"rows_loaded": len(df)})
        return len(df)


# Singleton instance
etl_service = ETLService()
