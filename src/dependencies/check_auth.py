from fastapi import Depends, HTTPException, Request, status
from src.database.core import get_db
from src.services.auth_session_service import get_auth_session
from src.services.user_service import get_user_by_id
from src.database.models import AuthSession, User
from datetime import datetime
from sqlalchemy.orm import Session

async def check_auth(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if not session: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else: 
        if session.expiry_datetime >= datetime.now():
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user: User = get_user_by_id(db, session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return session
