from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas.user_schemas import UserPublic
from bcrypt import hashpw, gensalt

def get_user(db: Session, username: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
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

def delete_user(db: Session, user_id: str, user: User):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if(user_to_delete):
        if(user_to_delete.id == user.id or (user.is_admin and user_to_delete.is_admin == False)):
            db.delete(user_to_delete)
            db.commit()
            return user_to_delete
        else: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User with id: {user.id} is not authorised to delete user with id: {user_id}.'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id: {user_id} not found.'
        )

def promote_user(db: Session, user_id: str, user: User) -> Optional[User]:
    user_to_promote = db.query(User).filter(User.id == user_id).first()
    if(user_to_promote):
        if(user.is_admin):
            user_to_promote.is_admin = True
            db.commit()
            db.refresh(user_to_promote)
            return user_to_promote
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User with id: {user.id} is not authorised to promote user with id: {user_id}.'
            )
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id: {user_id} not found.'
        )
    
def register_user(db: Session, username: str, password: str) -> Optional[User]:
    if(isBlank(username) or isBlank(password)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Username and password cannot be blank'
        )
    elif(len(password) < 8):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Password must be at least 8 characters long.'
        )
    
    existing_user = db.query(User).filter(User.username == username).first()
    if(existing_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Username {username} already in use.'
        )
    
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    
    new_user = User(username=username, password=hashed_password, is_admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

def isBlank(string: str):
    return not(string and string.strip())
