from app.db.sql_db import Base, engine
from app.models.sqlalchemy_models import UserModel

print("Creating tables…")
Base.metadata.create_all(bind=engine)
print("✅ Done")
