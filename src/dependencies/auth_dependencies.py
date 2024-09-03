from fastapi import Depends, HTTPException, Request, status
from src.database.core import get_db
from src.schemas.user_schemas import UserPublic
from src.services.auth_session_service import get_auth_session
from src.services.user_service import get_user_by_id
from src.database.models import AuthSession, User
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.handlers.auth_redirect_handler import AuthRedirect

#Get currently authenticated user based on sessionId 
async def get_user(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if session and session.expiry_datetime < datetime.now():
        user: User = get_user_by_id(db, session.user_id)
        return user
    return None

#Gets the user but omits sensitive information 
async def get_user_public(request: Request, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if user: 
        return UserPublic(**user.__dict__)  
    return None 

#Used to protect routes, checks if the sessionId is valid and associated with a user, else throws an exception 
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
    return user

#Used to protect routes similar to check_auth, but rather than throwing an exception, it redirects to the login page
async def check_auth_redirect(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("sessionId") or ""
    session: AuthSession = get_auth_session(db, session_id)
    if not session: 
        print("Session not found.")
        raise AuthRedirect()
    else: 
        if session.expiry_datetime >= datetime.now(timezone.utc):
            print("Session expired.")
            raise AuthRedirect()
    user: User = get_user_by_id(db, session.user_id)
    if not user:
        print("User not found.")
        raise AuthRedirect()
    return user