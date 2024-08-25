from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.database.models import User
from src.schemas.ticket_schemas import PostTicketRequest
from src.services.ticket_service import resolve_user_ticket, get_user_tickets, post_ticket, delete_user_ticket
from src.dependencies.auth_dependencies import check_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tickets", tags=["Ticket"])
async def get(user: User = Depends(check_auth), db: Session = Depends(get_db)):
    return get_user_tickets(db, user.id)

@router.post("/tickets", tags=["Ticket"])
async def post(post_ticket_request: PostTicketRequest, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    post_ticket(db, post_ticket_request.title, post_ticket_request.content, user.id)
    return {"message": "Succesfully added ticket."}

@router.delete("/tickets/{ticket_id}", tags=["Ticket"])
async def delete(ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    deleted_ticket = delete_user_ticket(db, ticket_id, user.id)
    if deleted_ticket:
        return {"message": "Succesfully deleted ticket."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ticket with id: ${id} not found.'
        )
    
@router.post("/tickets/resolve/{ticket_id}", tags=["Ticket"])
async def toggle_resolve(ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    resolved_ticket = resolve_user_ticket(db, ticket_id, user.id)
    if resolved_ticket:
        return {"message": "Succesfully resolved ticket."}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ticket with id: ${id} not found.'
        )
