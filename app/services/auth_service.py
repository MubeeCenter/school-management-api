from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.sqlalchemy_models import UserModel, Student
from app.models.pydantic import UserCreate, UserOut


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------------
    # Student Self-Registration
    # ----------------------------------------
    def register_user(self, user: UserCreate) -> UserOut:
        # Check if username already exists
        existing = (
            self.db.query(UserModel)
            .filter(UserModel.username == user.username)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")

        # Ensure student record exists in 'students' table
        student = (
            self.db.query(Student)
            .filter(Student.username == user.username)
            .first()
        )
        if not student:
            raise HTTPException(
                status_code=400,
                detail="Student record not found. Contact the administrator."
            )

        # Create user
        new_user = UserModel(
            username=user.username,
            password=hash_password(user.password),  # SAFE: hash_password handles 72-byte limit
            role="student"
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            # Link student → user
            student.user_id = new_user.id
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        return UserOut(
            id=new_user.id,
            username=new_user.username,
            role=new_user.role
        )

    # ----------------------------------------
    # LOGIN (OAuth2PasswordRequestForm)
    # ----------------------------------------
    def login_user(self, creds: OAuth2PasswordRequestForm):
        """
        Supports Swagger OAuth2 login form:
            username=...
            password=...
        """

        user = (
            self.db.query(UserModel)
            .filter(UserModel.username == creds.username)
            .first()
        )

        if not user:
            raise HTTPException(status_code=400, detail="Invalid username or password")

        # SAFE: verify_password handles truncation and bcrypt limits
        if not verify_password(creds.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        # Create token
        token = create_access_token(
            {"sub": user.username, "role": user.role}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role
        }

    # ----------------------------------------
    # ADMIN CREATES OTHER USERS (Lecturers/Admins)
    # ----------------------------------------
    def admin_register_user(self, user: UserCreate) -> UserOut:
        existing = (
            self.db.query(UserModel)
            .filter(UserModel.username == user.username)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = UserModel(
            username=user.username,
            role=user.role,
            password=hash_password(user.password)   # SAFE
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        return UserOut(
            id=new_user.id,
            username=new_user.username,
            role=new_user.role
        )
