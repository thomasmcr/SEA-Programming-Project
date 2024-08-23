from src.database.models import AuthSession
from sqlalchemy.orm import Session
from typing import Optional

def get_auth_session(db: Session, sessionId: str) -> Optional[Session]:
    return db.query(AuthSession).filter(AuthSession.id == sessionId).first()
