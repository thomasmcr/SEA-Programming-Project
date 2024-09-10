

from datetime import datetime
from src.dependencies.auth_dependencies import check_auth
from src.tests.test_main import test_client, clear_db, app, override_check_auth
from src.tests.test_utils import add_test_ticket_to_db, are_objects_equal, get_first_ticket, get_ticket_by_id

def test_update_ticket(clear_db):
    added_ticket = add_test_ticket_to_db()
    response = test_client.put(
        f"/tickets/{added_ticket.id}",
        json={"title": "new title", "content": "new content"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    ticket = data["ticket"]
    assert data["detail"] == "Succesfully updated ticket."

    assert "id" in ticket
    assert ticket["title"] == "new title"
    assert ticket["content"] == "new content"
    assert ticket["resolved"] is False
    assert datetime.fromisoformat(ticket["creation_datetime"]) <= datetime.utcnow()
    assert get_first_ticket() != None

def test_update_ticket_invalid(clear_db):
    response = test_client.put(
        f"/tickets/{-1}",
        json={"title": "title", "content": "content"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Ticket with id: -1 not found." 
    assert get_first_ticket() == None

def test_update_ticket_invalid_both_blank(clear_db):
    added_ticket = add_test_ticket_to_db()
    response = test_client.put(
        f"/tickets/{added_ticket.id}",
        json={"title": "", "content": ""},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Both the title and content cannot be blank." 
    assert are_objects_equal(added_ticket, get_ticket_by_id(added_ticket.id)) == True

def test_update_ticket_invalid_both_undefined(clear_db):
    added_ticket = add_test_ticket_to_db()
    response = test_client.put(
        f"/tickets/{added_ticket.id}",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Both the title and content cannot be blank." 
    assert are_objects_equal(added_ticket, get_ticket_by_id(added_ticket.id)) == True

def test_update_ticket_unauthorised(clear_db):
    app.dependency_overrides.pop(check_auth, None)
    response = test_client.put(
        f"/tickets/{-1}",
        json={"title": "title", "content": "content"},
    )
    app.dependency_overrides[check_auth] = override_check_auth
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorized" 
    assert get_first_ticket() == None
