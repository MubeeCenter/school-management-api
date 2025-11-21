from app.db.sql_db import SessionLocal
from app.models.sqlalchemy_models import UserModel
from app.core.security import hash_password

db = SessionLocal()

admin = UserModel(
    username="admin",
    password=hash_password("admin123"),   # change password if desired
    role="admin"
)

db.add(admin)
db.commit()
db.refresh(admin)

print("Admin created successfully:", admin.id)
