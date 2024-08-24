from src.database.models import Ticket
from sqlalchemy.orm import Session

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def post_ticket(db: Session, title: str, content: str):
    new_ticket = Ticket(title=title, content=content)
    db.add(new_ticket)
    db.commit()
    return new_ticket

def delete_ticket(db: Session, id: str):
    db.query(Ticket).filter(Ticket.id == id).delete()
    db.commit()

