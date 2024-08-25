from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, status
from src.database.core import get_db
from src.database.models import AuthSession
from src.schemas.ticket_schemas import PostTicketRequest
from src.services.ticket_service import *
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.dependencies.check_auth import check_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tickets", tags=["Ticket"])
async def get(req: Request, authSession: AuthSession = Depends(check_auth), db: Session = Depends(get_db)):
    return get_user_tickets(db, authSession.user_id)

@router.post("/tickets", tags=["Ticket"], dependencies=[Depends(check_auth)])
async def post(postTicketRequest: PostTicketRequest, request: Request, authSession = Depends(check_auth), db: Session = Depends(get_db)):
    post_ticket(db, postTicketRequest.title, postTicketRequest.content, authSession.user_id)
    return {"message": "Succesfully added ticket."}

@router.delete("/tickets", tags=["Ticket"])
async def delete(id: str, request: Request, authSession: AuthSession = Depends(check_auth), db: Session = Depends(get_db)):
    deleted_ticket = delete_user_ticket(db, id, authSession.user_id)
    if(deleted_ticket):
        return {"message": "Succesfully deleted ticket."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ticket with id: ${id} not found.'
        )
    
@router.post("/tickets/resolve", tags=["Ticket"])
async def toggle_resolve(id: str, request: Request, authSession: AuthSession = Depends(check_auth), db: Session = Depends(get_db)):
    resolved_ticket = resolve_user_ticket(db, id, authSession.user_id)
    if(resolved_ticket):
        return {"message": "Succesfully resolved ticket."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ticket with id: ${id} not found.'
        )


    




    