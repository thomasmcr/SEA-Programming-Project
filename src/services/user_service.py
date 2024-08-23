from src.database.models import AuthSession, User
from sqlalchemy.orm import Session
from typing import Optional

def post_user(username: str, passworD: str, db: Session):
    pass
    
def get_user(username: str, password: str, db: Session) -> Optional[User]:
    return db.query(User).filter(username == username).filter(password == password).first()

def refresh_session(user: User, db: Session):
    authSession = AuthSession(user=user)
    db.add(authSession)
    db.commit()
    return authSession