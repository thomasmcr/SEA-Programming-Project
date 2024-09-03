from fastapi import APIRouter, Cookie, Depends, Request, Response, HTTPException, status
from src.database.core import get_db
from src.services.user_service import get_user
from src.services.auth_session_service import refresh_session, delete_auth_session
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.schemas.user_schemas import LoginRequest

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/login", tags=["User"])
async def login(login_request: LoginRequest, req: Request, res: Response, db: Session = Depends(get_db)):
    user = get_user(db, login_request.username, login_request.password)
    session = refresh_session(user, db)
    res.set_cookie("sessionId", session.id)
    return {"message": "login success.", "sessionId": session.id}

@router.delete("/logout", tags=["User"])
async def logout(req: Request, res: Response, sessionId: str = Cookie(None), db: Session = Depends(get_db)):
    deleted_session = delete_auth_session(db, sessionId)
    if not deleted_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session with id: {id} not found.".format(id=sessionId)
        )
    res.delete_cookie("sessionId")
    return {"message": "succesfully logged out."}