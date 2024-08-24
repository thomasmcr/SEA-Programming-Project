from fastapi import APIRouter, Depends, Request
from src.database.core import get_db
from src.services.ticket_service import *
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.dependencies.check_auth import check_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tickets", tags=["Ticket"], dependencies=[Depends(check_auth)])
async def get(req: Request, db: Session = Depends(get_db)):
    return get_all_tickets(db)

@router.post("/tickets", tags=["Ticket"], dependencies=[Depends(check_auth)])
async def post(title: str, content: str, request: Request, db: Session = Depends(get_db)):
    post_ticket(db, title, content)
    return {"message": "Succesfully added ticket."}

@router.delete("/tickets", tags=["Ticket"], dependencies=[Depends(check_auth)])
async def delete(id: str, request: Request, db: Session = Depends(get_db)):
    delete_ticket(db, id)
    return {"message": "Succesfully deleted ticket."}




    