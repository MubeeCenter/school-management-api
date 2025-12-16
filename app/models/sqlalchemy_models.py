from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, Index
from sqlalchemy.orm import relationship
from app.db.sql_db import Base

# =====================================================
#   USERS TABLE
# =====================================================
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, default="student")

    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)

    student = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        lazy="joined",
        viewonly=True
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_user_username", "username"),
    )


# =====================================================
#   STUDENTS TABLE
# =====================================================
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True)
    username = Column(String, nullable=True)

    user = relationship(
        "UserModel",
        back_populates="student",
        uselist=False,
        lazy="joined",
        viewonly=True
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_student_email", "email"),
    )


# =====================================================
#   LECTURERS TABLE
# =====================================================
class Lecturer(Base):
    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)

    courses = relationship(
        "Course",
        back_populates="lecturer",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# =====================================================
#   COURSES TABLE
# =====================================================
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    semester = Column(String, nullable=False)
    credits = Column(Integer, default=3)
    lecturer_id = Column(Integer, ForeignKey("lecturers.id"), nullable=True)

    lecturer = relationship("Lecturer", back_populates="courses")

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_course_code", "code"),
    )


# =====================================================
#   ENROLLMENTS TABLE
# =====================================================
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    grade = Column(Float, nullable=True)
    gpa = Column(Float, nullable=True)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_enrollments_student", "student_id"),
        Index("idx_enrollments_course", "course_id"),
    )
# =====================================================
#   GRADES TABLE ✅ (NEW)
# =====================================================
class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    score = Column(Float, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        Index("idx_grade_student", "student_id"),
        Index("idx_grade_course", "course_id"),
    )
__table_args__ = (
    Index("uq_student_course", "student_id", "course_id", unique=True),
)
role = Column(String, default="student", nullable=False)
