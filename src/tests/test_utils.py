
from src.dependencies.auth_dependencies import check_auth
from src.tests.test_main import session
from src.database.models import Ticket, User


def add_test_ticket_to_db(title: str = "title", content: str = "content"):
    ticket = Ticket(title="title", content="content", author_id=0)
    db = session()
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def add_test_user_to_db(id: int = 1, username: str = "username", password: str = "password", is_admin: bool = False):
    user = User(id=id, username=username, password=password, is_admin=is_admin)
    db = session()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_ticket_by_id(ticket_id: str):
    db = session()
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_user_by_id(user_id: str):
    db = session()
    return db.query(User).filter(User.id == user_id).first()

def are_objects_equal(obj1, obj2, exclude_fields = []):
    keys1 = {key for key in obj1.__dict__.keys() if not key.startswith('_') and key not in exclude_fields}
    keys2 = {key for key in obj2.__dict__.keys() if not key.startswith('_') and key not in exclude_fields}
    
    # First, check if both objects have the same set of keys (excluding any fields as specified)
    if keys1 != keys2:
        return False

    # Now check if all values corresponding to these keys are equal
    for key in keys1:
        if getattr(obj1, key) != getattr(obj2, key):
            return False

    return True  