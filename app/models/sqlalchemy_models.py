from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.sql_db import Base


# ===========================
#   USERS TABLE
# ===========================
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, default="student")

    # One-to-one relationship with Student
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    student = relationship("Student", back_populates="user")


# ===========================
#   STUDENTS TABLE
# ===========================
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True, nullable=True)

    # Relationship back to User
    user = relationship("UserModel", back_populates="student", uselist=False)

    # Relationship to Enrollments
    enrollments = relationship("Enrollment", back_populates="student")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "username": self.username,
        }


# ===========================
#   LECTURERS TABLE
# ===========================
class Lecturer(Base):
    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)

    # One-to-many: a lecturer can teach multiple courses
    courses = relationship("Course", back_populates="lecturer")


# ===========================
#   COURSES TABLE
# ===========================
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    semester = Column(String, nullable=False)
    lecturer_id = Column(Integer, ForeignKey("lecturers.id"), nullable=True)

    # Relationship back to Lecturer
    lecturer = relationship("Lecturer", back_populates="courses")

    # Relationship to Enrollments
    enrollments = relationship("Enrollment", back_populates="course")


# ===========================
#   ENROLLMENTS TABLE
# ===========================
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    grade = Column(Float)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
