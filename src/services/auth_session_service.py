from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import AuthSession, User

def get_auth_session(db: Session, session_id: str) -> Optional[Session]:
    return db.query(AuthSession).filter(AuthSession.id == session_id).first()

def refresh_session(user: User, db: Session) -> AuthSession:
    #Delete old session 
    db.query(AuthSession).filter(AuthSession.user_id == user.id).delete()
    db.commit()

    #Create new session
    auth_session = AuthSession(user=user)
    db.add(auth_session)
    db.commit()
    db.refresh(auth_session)
    return auth_session

def delete_auth_session(db: Session, session_id: str) -> Optional[Session]:
    session_to_delete = db.query(AuthSession).filter(AuthSession.id == session_id).first()
    if session_to_delete:
        db.delete(session_to_delete)
        db.commit()
        return session_to_delete
    return None
