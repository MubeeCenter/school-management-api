from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ------------------------------------
    # 🔐 Security
    # ------------------------------------
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ------------------------------------
    # 🗃 SQL Database
    # ------------------------------------
    SQLALCHEMY_DATABASE_URL: str

    # ------------------------------------
    # 🍃 MongoDB (Analytics Database)
    # ------------------------------------
    MONGO_URI: str
    MONGO_DB_NAME: str = "school_analytics"

    # Collections
    MONGO_COLLECTION_STUDENTS: str = "dimStudents"
    MONGO_COLLECTION_COURSES: str = "dimCourses"
    MONGO_COLLECTION_LECTURERS: str = "dimLecturers"
    MONGO_COLLECTION_FACTS: str = "factEnrollments"
    MONGO_COLLECTION_PREDICTIONS: str = "predictions"

    # ------------------------------------
    # 📬 Email / Alerts
    # ------------------------------------
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 465
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    # ------------------------------------
    # 🌐 CORS
    # ------------------------------------
    CORS_ORIGINS: List[str] = ["*"]

    # ------------------------------------
    # 🛠 Environment
    # ------------------------------------
    ENV: str = "dev"   # dev | prod

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global instance
settings = Settings()
