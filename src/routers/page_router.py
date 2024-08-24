from fastapi import APIRouter, Depends, Request
from src.database.core import get_db
from src.services.ticket_service import * 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.dependencies.check_auth import check_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["Pages"])
async def home(req: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=req, name="/pages/home.html", context={"page": "/"}
    )

@router.get("/my-tickets-page", tags=["Pages"])
async def view_my_tickets(req: Request, db: Session = Depends(get_db)):
    tickets = get_all_tickets(db)
    return templates.TemplateResponse(
        request=req, name="/pages/my_tickets.html", context={"page": "/my-tickets", "tickets": tickets}
    )

@router.get("/unauthorised-page", tags=["Pages"])
async def unauthorised(req: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=req, name="/pages/unauthorised.html", context={"page": "/unauthorised"}
    )