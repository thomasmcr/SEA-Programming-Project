from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas.user_schemas import UserPublic

def get_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )
    return user 

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_public_users(db: Session, exclude_user_ids: Optional[list[str]] = []) -> List[UserPublic]:
    users = db.query(User).filter(User.id.not_in(exclude_user_ids)).all()
    public_users = [UserPublic(**user.__dict__) for user in users]
    return public_users

