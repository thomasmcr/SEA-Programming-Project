from fastapi import APIRouter, Depends, Query, Request
from src.database.core import get_db
from src.services.ticket_service import * 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.models import AuthSession
from src.dependencies.check_auth_page import check_auth_page

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["Pages"])
async def home(req: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=req, name="/pages/home.html", context={"page": "/"}
    )

@router.get("/my-tickets-page", tags=["Pages"])
async def view_my_tickets(req: Request, authSession: AuthSession = Depends(check_auth_page), db: Session = Depends(get_db)):
    tickets = get_user_tickets(db, authSession.user_id)
    return templates.TemplateResponse(
        request=req, name="/pages/my_tickets.html", context={"page": "/my-tickets-page", "tickets": tickets}
    )

@router.get("/unauthorised-page", tags=["Pages"])
async def unauthorised(req: Request, old_location: str = Query("old_location"), db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=req, name="/pages/unauthorised.html", context={"page": old_location}
    )