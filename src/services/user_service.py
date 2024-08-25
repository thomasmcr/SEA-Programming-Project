from src.database.models import AuthSession, User
from sqlalchemy.orm import Session
from typing import Optional

def post_user(username: str, password: str, db: Session):
    pass
    
def get_user(db: Session, username: str, password: str) -> Optional[User]:
    return db.query(User).filter(User.username == username, User.password == password).first()

def get_user_by_id(db: Session, userId: str) -> Optional[User]:
    return db.query(User).filter(User.id == userId).first()
    
