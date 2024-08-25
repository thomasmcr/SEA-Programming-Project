from fastapi import Depends, HTTPException, Request, status
from src.database.core import get_db
from src.services.auth_session_service import get_auth_session
from src.database.models import AuthSession
from datetime import datetime
from sqlalchemy.orm import Session

class AuthRedirect(Exception):
    def __init__(self, name: str = "AuthRedirect"):
        self.name = name

async def check_auth_page(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if not session: 
        raise AuthRedirect()
    else: 
        if session.expiry_datetime >= datetime.now():
            raise AuthRedirect()
    return session

