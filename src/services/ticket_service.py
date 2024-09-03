from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import case
from src.database.models import Ticket, User
from src.schemas.user_schemas import UserPublic

def post_ticket(db: Session, title: str, content: str, user_id: str) -> Ticket:
    if(not title or not content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="title and content strings cannot be blank."
        )
    new_ticket = Ticket(title=title, content=content, author=user_id)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def delete_ticket(db: Session, ticket_id: str, user: UserPublic):
    ticket_to_delete = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if(ticket_to_delete):
        if(ticket_to_delete.author == user.id or user.is_admin):
            db.delete(ticket_to_delete)
            db.commit()
            return ticket_to_delete
        else: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User with id: {user.id} is not authorised to delete ticket with id: {ticket_id}.'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ticket with id: {ticket_id} not found.'
        )

def resolve_ticket(db: Session, ticket_id: str, user: UserPublic):
    ticket_to_resolve = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if(ticket_to_resolve):
        if(ticket_to_resolve.author == user.id or user.is_admin):
            ticket_to_resolve.resolved = True
            db.commit()
            db.refresh(ticket_to_resolve)
            return ticket_to_resolve
        else: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User with id: {user.id} is not authorised to resolve ticket with id: {ticket_id}.'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ticket with id: {ticket_id} not found.'
        )
        
def get_user_tickets(db: Session, user_id: str) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.author == user_id).order_by(Ticket.creation_datetime.desc()).all()

def get_all_tickets(db: Session) -> List[Ticket]:
    return db.query(Ticket).all()

def get_all_unresolved_tickets(db: Session, user_id: str) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.resolved == False, Ticket.author != user_id).all()

def get_ticket_by_id(db: Session, ticket_id: str, user: UserPublic):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()
