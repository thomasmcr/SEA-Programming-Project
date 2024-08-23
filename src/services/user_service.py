from src.database.models import AuthSession, User
from sqlalchemy.orm import Session
from typing import Optional

def post_user(username: str, password: str, db: Session):
    pass
    
def get_user(username: str, password: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.username == username, User.password == password).first()

def refresh_session(user: User, db: Session):
    #Delete old session 
    db.query(AuthSession).filter(AuthSession.user_id == user.id).delete()
    db.commit()

    #Create new session
    authSession = AuthSession(user=user)
    db.add(authSession)
    db.commit()
    db.refresh(authSession)
    return authSession