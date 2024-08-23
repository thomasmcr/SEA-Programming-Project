from fastapi import APIRouter, Depends, Request
from src.database.core import get_db
from src.services.ticket_service import *
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tickets", tags=["Ticket"])
async def get_tickets(req: Request, db: Session = Depends(get_db)):
    return get_all_tickets(db)

@router.post("/tickets", tags=["Ticket"])
async def post_ticket(title: str, content: str, request: Request, db: Session = Depends(get_db)):
    post_ticket(db, title, content)
    return {"message": "Succesfully added ticket."}



    