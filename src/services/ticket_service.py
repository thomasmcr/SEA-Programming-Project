from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case
from src.database.models import Ticket

def get_all_tickets(db: Session) -> List[Ticket]:
    return db.query(Ticket).all()

def post_ticket(db: Session, title: str, content: str, userId: str) -> Ticket:
    new_ticket = Ticket(title=title, content=content, author=userId)
    db.add(new_ticket)
    db.commit()
    return new_ticket

def delete_ticket(db: Session, id: str):
    ticket_to_delete = db.query(Ticket).filter(Ticket.id == id).first()
    if ticket_to_delete: 
        db.delete(ticket_to_delete)
        db.commit()
    return ticket_to_delete

def get_user_tickets(db: Session, userId: str):
    return db.query(Ticket).filter(Ticket.author == userId).order_by(case((Ticket.resolved == False, 0), else_=1)).all()

def delete_user_ticket(db: Session, ticketId: str, userId: str) -> Optional[Ticket]:
    ticket_to_delete = db.query(Ticket).filter(Ticket.id == ticketId, Ticket.author == userId).first()
    if ticket_to_delete:
        db.delete(ticket_to_delete)
        db.commit()
    return ticket_to_delete

def resolve_user_ticket(db: Session, ticketId: str, userId: str) -> Optional[Ticket]:
    ticket_to_resolve = db.query(Ticket).filter(Ticket.id == ticketId, Ticket.author == userId).first()
    if ticket_to_resolve:
        ticket_to_resolve.resolved = True
        db.commit()
        db.refresh(ticket_to_resolve)
    return ticket_to_resolve
