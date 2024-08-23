from fastapi import Depends, HTTPException, Request, status
from src.database.core import get_db
from src.services.auth_session_service import get_auth_session
from src.database.models import AuthSession
from datetime import datetime
from sqlalchemy.orm import Session

async def check_auth(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if not session: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token"
        )
    else: 
        if session.expiry_datetime >= datetime.now():
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token expired"
        )

