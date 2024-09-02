

from src.tests.test_main import test_client, clear_db, app, override_check_auth
from src.tests.test_utils import add_test_ticket_to_db, get_ticket_by_id, are_objects_equal
from src.dependencies.auth_dependencies import check_auth

def test_delete_ticket_valid(clear_db):
    added_ticket = add_test_ticket_to_db()
    response = test_client.delete(
        f'/tickets/{added_ticket.id}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    ticket = data["ticket"]
    assert data["detail"] == "Succesfully deleted ticket."
    assert ticket["id"] == added_ticket.id
    assert get_ticket_by_id(added_ticket.id) == None

def test_delete_ticket_invalid(clear_db):
    ticket_id = -1
    response = test_client.delete(
        f'/tickets/{ticket_id}'
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f'Ticket with id: {ticket_id} not found.'

def test_delete_ticket_unauthorised(clear_db):
    app.dependency_overrides.pop(check_auth, None) #Remove auth override 
    added_ticket = add_test_ticket_to_db()
    response = test_client.delete(
        f'/tickets/{added_ticket.id}'
    )
    app.dependency_overrides[check_auth] = override_check_auth
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorized"
    assert are_objects_equal(added_ticket, get_ticket_by_id(added_ticket.id)) == True
 
    