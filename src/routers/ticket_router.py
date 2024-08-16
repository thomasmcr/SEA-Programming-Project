from fastapi import APIRouter, Depends, Request
from src.database.core import get_db
from src.database.models import Ticket
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tickets", tags=["Ticket"])
async def view_tickets(request: Request, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return tickets

@router.post("/tickets", tags=["Ticket"])
async def post_ticket(title: str, content: str, request: Request, db: Session = Depends(get_db)):
    new_ticket = Ticket(title=title, content=content)
    db.add(new_ticket)
    db.commit()
    return {"message": "Succesfully added ticket!"}



    