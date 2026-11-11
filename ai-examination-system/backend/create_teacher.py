
from getpass import getpass

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.enums import UserRole
from app.models.user import User


name = input("Teacher name: ")
email = input("Teacher email: ")
password = getpass("Teacher password: ")
confirm_password = getpass("Confirm password: ")

if password != confirm_password:
    raise ValueError("Passwords do not match")

db = SessionLocal()

try:
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise ValueError("Email already exists")

    teacher = User(
        name=name,
        email=email,
        password=hash_password(password),
        role=UserRole.TEACHER
    )

    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    print("Teacher account created successfully")
    print("Teacher ID:", teacher.id)

except Exception:
    db.rollback()
    raise

finally:
    db.close()
