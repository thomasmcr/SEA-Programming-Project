from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import User

def get_user(db: Session, username: str, password: str) -> Optional[User]:
    return db.query(User).filter(User.username == username, User.password == password).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
