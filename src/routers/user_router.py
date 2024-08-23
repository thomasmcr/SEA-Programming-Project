from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from src.database.core import get_db
from src.services.user_service import *
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.schemas.user_schemas import LoginRequest

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/login", tags=["User"])
async def login(login_request: LoginRequest, req: Request, res: Response, db: Session = Depends(get_db)):
    user = get_user(login_request.username, login_request.password, db)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    session = refresh_session(user, db)
    res.set_cookie("sessionId", session.id)
    return {"message": "login success.", "sessionId": session.id}


@router.post("/register", tags=["User"])
async def register(db: Session = Depends(get_db)):
   return {"message": "not implemented yet!"}