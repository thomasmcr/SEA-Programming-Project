from fastapi import APIRouter, Depends, Request, Response
from src.database.core import get_db
from src.services.ticket_service import * 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", tags=["Pages"])
async def view_all_tickets(req: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=req, name="/pages/home_page.html", context={"page": "/"}
    )

@router.get("/my-tickets", tags=["Pages"])
async def view_my_tickets(req: Request, db: Session = Depends(get_db)):
    tickets = get_all_tickets(db)
    return templates.TemplateResponse(
        request=req, name="/pages/my_tickets_page.html", context={"page": "/my-tickets", "tickets": tickets}
    )