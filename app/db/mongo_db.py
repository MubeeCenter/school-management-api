# app/db/mongo_db.py
from pymongo import MongoClient, errors
from app.config import settings


def get_mongo_client() -> MongoClient | None:
    """
    Initialize MongoDB connection using URI from settings.
    Returns a MongoClient if successful, otherwise None.
    """
    try:
        # Recommended Atlas connection options
        client = MongoClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=8000,   # wait 8s for connection
            retryWrites=True
        )
        # Ping to confirm connectivity
        client.admin.command("ping")
        print("✅ Connected to MongoDB successfully!")
        return client

    except errors.ServerSelectionTimeoutError as e:
        print(f"❌ MongoDB connection failed (timeout): {e}")
    except errors.ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected MongoDB error: {e}")
    
    return None  # allow rest of app to continue even if Mongo is down


# Initialize the client globally once
client = get_mongo_client()

if client:
    db = client["school_analytics"]

    # Define collections
    students_col = db["dimStudents"]
    courses_col = db["dimCourses"]
    lecturers_col = db["dimLecturers"]
    facts_col = db["factEnrollments"]
else:
    print("⚠️ MongoDB unavailable. Falling back to SQL-only mode.")
    students_col = courses_col = lecturers_col = facts_col = None
