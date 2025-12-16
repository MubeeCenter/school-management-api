from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user


def get_current_student(user = Depends(get_current_user)):
    if user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Students only"
        )
    return user


def get_current_admin(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user
