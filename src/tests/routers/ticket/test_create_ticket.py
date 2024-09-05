

from datetime import datetime
from src.dependencies.auth_dependencies import check_auth
from src.tests.test_main import test_client, clear_db, app, override_check_auth

def test_create_ticket(clear_db):
    response = test_client.post(
        "/tickets/",
        json={"title": "title", "content": "content"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    ticket = data["ticket"]
    assert data["detail"] == "Succesfully added ticket."

    assert "id" in ticket
    assert ticket["title"] == "title"
    assert ticket["content"] == "content"
    assert ticket["resolved"] is False
    assert datetime.fromisoformat(ticket["creation_datetime"]) <= datetime.utcnow()

def test_create_ticket_unauthorised(clear_db):
    app.dependency_overrides.pop(check_auth, None)
    response = test_client.post(
        "/tickets/",
        json={"title": "title", "content": "content"},
    )
    app.dependency_overrides[check_auth] = override_check_auth
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorized"
 
    