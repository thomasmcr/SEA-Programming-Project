from src.database.models import AuthSession, User
from sqlalchemy.orm import Session
from typing import Optional

def get_auth_session(db: Session, sessionId: str) -> Optional[Session]:
    return db.query(AuthSession).filter(AuthSession.id == sessionId).first()

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

def delete_auth_session(db: Session, sessionId: str) -> Optional[Session]:
    session_to_delete = db.query(AuthSession).filter(AuthSession.id == sessionId).first()
    if session_to_delete:
        db.delete(session_to_delete)
        db.commit()
        return session_to_delete
    return None