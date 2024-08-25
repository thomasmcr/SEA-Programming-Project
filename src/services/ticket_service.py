from typing import Optional
from src.database.models import Ticket
from sqlalchemy.orm import Session

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def get_user_tickets(db: Session, userId: str):
    return db.query(Ticket).filter(Ticket.author == userId).all()

def post_ticket(db: Session, title: str, content: str, userId: str):
    new_ticket = Ticket(title=title, content=content, author=userId)
    db.add(new_ticket)
    db.commit()
    return new_ticket

def delete_ticket(db: Session, id: str):
    db.query(Ticket).filter(Ticket.id == id).delete()
    db.commit()

def delete_user_ticket(db: Session, ticketId: str, userId: str) -> Optional[Ticket]:
    ticket_to_delete = db.query(Ticket).filter(Ticket.id == ticketId, Ticket.author == userId).first()
    db.delete(ticket_to_delete)
    db.commit()
    return ticket_to_delete