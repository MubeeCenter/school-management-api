from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
from app.models.sqlalchemy_models import UserModel
from app.models.pydantic import UserCreate, UserLogin
from sqlalchemy.orm import Session

class AuthService:
    """Handles user registration, login, and JWT token management."""

    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user: UserCreate) -> dict:
        """Register a new user with a hashed password."""
        existing_user = self.db.query(UserModel).filter(UserModel.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_pwd = hash_password(user.password)
        new_user = UserModel(username=user.username, password=hashed_pwd, role=user.role)

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        return {"message": f"User '{user.username}' registered successfully!"}

    def login_user(self, user: UserLogin) -> dict:
        """Authenticate user and return a JWT token."""
        db_user = self.db.query(UserModel).filter(UserModel.username == user.username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": db_user.username, "role": db_user.role})
        return {"access_token": token, "token_type": "bearer"}
