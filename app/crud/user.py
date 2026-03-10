from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password

def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def create_user(db: Session, username: str, password: str, age: int) -> User:
    user = User(username=username, hashed_password=hash_password(password), age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user