from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🔐 Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🗃 SQL Database
    SQLALCHEMY_DATABASE_URL: str

    # 🍃 MongoDB (Analytics DB)
    MONGO_URI: str
    MONGO_DB_NAME: str = "school_analytics"   # default, can be overridden in Railway

    # 📊 MongoDB Collections
    MONGO_COLLECTION_STUDENTS: str = "dimStudents"
    MONGO_COLLECTION_COURSES: str = "dimCourses"
    MONGO_COLLECTION_LECTURERS: str = "dimLecturers"
    MONGO_COLLECTION_FACTS: str = "factEnrollments"

    class Config:
        env_file = ".env"      # Load from local .env when running locally
        case_sensitive = True


# Global settings instance
settings = Settings()
