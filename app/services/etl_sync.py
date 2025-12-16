"""
etl_sync.py

Full CSV → MongoDB ETL for school analytics.
Author: Mubarak (generated with ChatGPT)

✔ Reads:
    - factEnrollments.csv
    - dimStudents.csv
    - dimCourses.csv
    - dimLecturers.csv

✔ Cleans + transforms data:
    - Trim strings
    - Convert GPA to float
    - Map grades (A, B+, etc.)
    - Add Year (from Semester text or default)
    - Add Status (Active/Inactive based on GPA)

✔ Loads to MongoDB:
    - Database: school_analytics
    - Collection: factEnrollments
    - Optional: delete existing docs before inserting (--clean)

Usage:
    python etl_sync.py --csv factEnrollments.csv --clean
"""

import argparse
import os
import re
from pathlib import Path
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")


# -------------------------------
# Helpers
# -------------------------------

def clean_string(val):
    """Trim strings safely."""
    if pd.isna(val):
        return None
    return str(val).strip()


def extract_year(semester):
    """Extract a 4-digit year from text like 'Harmattan 2023'."""
    if pd.isna(semester):
        return None
    parts = re.split(r"[\s,_\-/]+", str(semester))
    for p in parts:
        if p.isdigit() and len(p) == 4:
            return int(p)
    return None


def determine_status(gpa, threshold=1.0):
    """Return Active if GPA >= threshold."""
    try:
        return "Active" if float(gpa) >= threshold else "Inactive"
    except:
        return "Active"


def grade_to_gpa(val):
    """Convert letter grades to numeric GPA."""
    if val is None:
        return 0.0

    try:
        # If already numeric, convert directly
        return float(val)
    except:
        grade = str(val).strip().upper()
        mapping = {
            "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D": 1.0,
            "F": 0.0,
        }
        return mapping.get(grade, 0.0)


def load_csv(path):
    """Load CSV safely."""
    path = Path(path)
    if not path.exists():
        logging.error(f"CSV file not found: {path}")
        return None
    df = pd.read_csv(path, dtype=str)
    logging.info(f"Loaded {len(df)} rows from {path.name}")
    return df


# -------------------------------
# Main ETL
# -------------------------------

def main(args):
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DB", "school_analytics")
    fact_collection = os.getenv("FACT_COLLECTION", "factEnrollments")

    if not mongo_uri:
        logging.error("❌ MONGO_URI missing in .env file")
        return

    # Load main fact table
    fact_df = load_csv(args.csv)
    if fact_df is None:
        logging.error("❌ No input file loaded. Exiting.")
        return

    # Standardize columns
    fact_df.columns = [c.strip() for c in fact_df.columns]

    # Detect columns
    col_map = {
        "StudentID": None,
        "CourseName": None,
        "Semester": None,
        "GPA": None,
        "Lecturer": None,
    }

    for col in fact_df.columns:
        c = col.lower()
        if "student" in c:
            col_map["StudentID"] = col
        elif "course" in c:
            col_map["CourseName"] = col
        elif "semester" in c:
            col_map["Semester"] = col
        elif "gpa" in c or "grade" in c:
            col_map["GPA"] = col
        elif "lecturer" in c or "teacher" in c or "instructor" in c:
            col_map["Lecturer"] = col

    logging.info(f"🔍 Column mapping detected: {col_map}")

    # Validation
    required_cols = ["StudentID", "CourseName", "Semester"]
    for r in required_cols:
        if col_map[r] is None:
            raise Exception(f"Required column missing in CSV: {r}")

    # Transform rows
    records = []
    for _, row in fact_df.iterrows():
        student_id = clean_string(row[col_map["StudentID"]])
        course = clean_string(row[col_map["CourseName"]])
        semester = clean_string(row[col_map["Semester"]])

        # GPA conversion
        gpa_raw = row[col_map["GPA"]] if col_map["GPA"] else None
        gpa = grade_to_gpa(gpa_raw)

        # Year
        year = extract_year(semester) or args.default_year

        # Status
        status = determine_status(gpa, threshold=args.active_threshold)

        rec = {
            "StudentID": student_id,
            "Course": course,
            "Semester": semester,
            "GPA": gpa,
            "Lecturer": clean_string(row[col_map["Lecturer"]]) if col_map["Lecturer"] else None,
            "Year": int(year),
            "Status": status,
        }
        records.append(rec)

    logging.info(f"Transformed {len(records)} records… inserting into MongoDB…")

    # ---------------------------
    # MongoDB Insert
    # ---------------------------

    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    coll = db[fact_collection]

    if args.clean:
        logging.info("🧹 Cleaning existing data...")
        coll.delete_many({})

    # Insert in batches
    batch_size = 500
    for i in range(0, len(records), batch_size):
        coll.insert_many(records[i:i + batch_size])
        logging.info(f"Inserted batch {i} → {i + batch_size}")

    logging.info("✅ ETL Complete!")


# -------------------------------
# Entry Point
# -------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full CSV → MongoDB ETL")
    parser.add_argument("--csv", required=True, help="Path to factEnrollments CSV")
    parser.add_argument("--default-year", type=int, default=2024)
    parser.add_argument("--active-threshold", type=float, default=1.0)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    main(args)
