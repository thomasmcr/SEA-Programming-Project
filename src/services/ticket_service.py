from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.database.models import Comment, Ticket
from src.schemas.user_schemas import UserPublic

def post_ticket(db: Session, title: str, content: str, user_id: str) -> Ticket:
    if(isBlank(title) or isBlank(content)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and content strings cannot be blank."
        )
    new_ticket = Ticket(title=title, content=content, author_id=user_id)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def delete_ticket(db: Session, ticket_id: str, user: UserPublic):
    ticket_to_delete = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if(ticket_to_delete):
        if(ticket_to_delete.author_id == user.id or user.is_admin):
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
        if(ticket_to_resolve.author_id == user.id or user.is_admin):
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

def update_ticket(db: Session, ticket_id: str, new_title: Optional[str], new_content: Optional[str], user: UserPublic):
    ticket_to_update = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if(ticket_to_update):
        if(ticket_to_update.author_id == user.id or user.is_admin):
            if(ticket_to_update.resolved == True):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'Cannot update ticket: {ticket_id} as it is resolved.'
                )
            if(new_title):
                ticket_to_update.title = new_title
            if (new_content):
                ticket_to_update.content = new_content
            db.commit()
            db.refresh(ticket_to_update)
            return ticket_to_update
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User with id: {user.id} is not authorised to update ticket with id: {ticket_id}.'
            )
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ticket with id: {ticket_id} not found.'
        )
    
def add_comment(db: Session, ticket_id: str, content: str, user: UserPublic):
    if(isBlank(content)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content string cannot be blank."
        )
    
    ticket = get_ticket_by_id(db, ticket_id, user)
    if(ticket):
        if(ticket.author_id == user.id or user.is_admin):
            new_comment = Comment(content=content, ticket_id=ticket_id, author_id=user.id)
            db.add(new_comment)
            db.commit()
            db.refresh(new_comment)
            return new_comment
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User with id: {user.id} is not authorised to add comment to ticket with id: {ticket_id}.'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ticket with id: {ticket_id} not found.'
        )
        
def get_user_tickets(db: Session, user_id: str) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.author_id == user_id).order_by(Ticket.creation_datetime.desc()).all()

def get_all_tickets(db: Session) -> List[Ticket]:
    return db.query(Ticket).all()

def get_all_unresolved_tickets(db: Session, user_id: str) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.resolved == False, Ticket.author_id != user_id).all()

def get_ticket_by_id(db: Session, ticket_id: str, user: UserPublic) -> Ticket:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def isBlank(string: str):
    return not(string and string.strip())