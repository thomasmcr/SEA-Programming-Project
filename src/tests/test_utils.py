
from src.dependencies.auth_dependencies import check_auth
from src.tests.test_main import session
from src.database.models import Ticket


def add_test_ticket_to_db(title: str = "title", content: str = "content", author: int = 0):
    ticket = Ticket(title="title", content="content", author=0)
    db = session()
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.close()
    return ticket

def get_ticket_by_id(ticket_id: str):
    db = session()
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def are_objects_equal(obj1, obj2, exclude_fields = []):
    for key in obj1.__dict__.keys():
        if key.startswith('_') or key in exclude_fields:
            continue

        if getattr(obj1, key) != getattr(obj2, key):
            return False
    return True    