from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.core import get_db
from src.database.models import User
from src.schemas.ticket_schemas import PostCommentRequest, PostTicketRequest, UpdateTicketRequest
from src.services.ticket_service import add_comment, get_user_tickets, post_ticket, resolve_ticket, delete_ticket, get_ticket_by_id, update_ticket
from src.dependencies.auth_dependencies import check_auth

router = APIRouter()

@router.get("/", tags=["Ticket"])
async def get(user: User = Depends(check_auth), db: Session = Depends(get_db)):
    return get_user_tickets(db, user.id)

@router.post("/", tags=["Ticket"])
async def post(post_ticket_request: PostTicketRequest, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    new_ticket = post_ticket(db, post_ticket_request.title, post_ticket_request.content, user.id)
    return {"detail": "Succesfully added ticket.", "ticket": new_ticket}

@router.get("/{ticket_id}", tags=["Ticket"])
async def get_by_id(ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    return get_ticket_by_id(db, ticket_id, user)

@router.put("/{ticket_id}", tags=["Ticket"])
async def update(update_ticket_request: UpdateTicketRequest, ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):

    if isBlank(update_ticket_request.title) and isBlank(update_ticket_request.content):
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both the title and content cannot be blank."
        )
    updated_ticket = update_ticket(db, ticket_id, update_ticket_request.title, update_ticket_request.content, user)
    if updated_ticket:
        return {"detail": "Succesfully updated ticket.", "ticket": updated_ticket}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to update ticket with id {ticket_id}. Please try again.'
        )

@router.delete("/{ticket_id}", tags=["Ticket"])
async def delete(ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    deleted_ticket = delete_ticket(db, ticket_id, user)
    if deleted_ticket:
        return {"detail": "Succesfully deleted ticket.", "ticket": deleted_ticket}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to delete ticket with id {ticket_id}. Please try again.'
        )
    
@router.put("/resolve/{ticket_id}", tags=["Ticket"])
async def resolve(ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    resolved_ticket = resolve_ticket(db, ticket_id, user)
    if resolved_ticket:
        return {"detail": "Succesfully resolved ticket.", "ticket": resolved_ticket}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to resolve ticket with id {ticket_id}. Please try again.'
        )
    
@router.post("/comment/{ticket_id}", tags=["Ticket"])
async def comment(post_comment_request: PostCommentRequest, ticket_id: str, user: User = Depends(check_auth), db: Session = Depends(get_db)):
    new_comment = add_comment(db, ticket_id, post_comment_request.content, user)
    if new_comment:
        return {"detail": "Succesfully added comment.", "comment": new_comment}
    else: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to add comment to ticket with id {ticket_id}. Please try again.'
        )
    
def isBlank(string: str):
    return not(string and string.strip())