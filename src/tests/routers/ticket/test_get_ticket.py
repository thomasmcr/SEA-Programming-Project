from src.tests.test_main import test_client, clear_db
from src.tests.test_utils import add_test_ticket_to_db

def test_get_all_user_tickets(clear_db):
    added_ticket_one = add_test_ticket_to_db(title="title-1")
    added_ticket_two = add_test_ticket_to_db(title="title-2")
    response = test_client.get(
        f'/tickets/'
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["id"] == added_ticket_one.id
    assert data[0]["id"] == added_ticket_two.id

def test_get_ticket(clear_db):
    added_ticket = add_test_ticket_to_db()
    response = test_client.get(
        f'/tickets/{added_ticket.id}'
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == added_ticket.id
    
##TODO add tests for unauthorised and invalid
