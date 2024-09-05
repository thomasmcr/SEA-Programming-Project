from fastapi import Depends, HTTPException, Request, status
from src.database.core import get_db
from src.services.auth_session_service import get_auth_session
from src.services.user_service import get_user_by_id
from src.database.models import AuthSession, User
from sqlalchemy.orm import Session
from src.handlers.auth_redirect_handler import AuthRedirect

#Get currently authenticated user based on sessionId 
async def get_user(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if session:
        user: User = get_user_by_id(db, session.user_id)
        return user
    return None

#Used to protect routes, checks if the sessionId is valid and associated with a user, else throws an exception 
async def check_auth(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if not session: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user: User = get_user_by_id(db, session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return user

#Used to protect routes similar to check_auth, but rather than throwing an exception, it redirects to the login page
async def check_auth_redirect(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if not session: 
        raise AuthRedirect()
    user: User = get_user_by_id(db, session.user_id)
    if not user:
        raise AuthRedirect()
    return user