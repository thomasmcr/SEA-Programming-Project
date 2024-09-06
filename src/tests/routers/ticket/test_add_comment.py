

from datetime import datetime
from src.dependencies.auth_dependencies import check_auth
from src.tests.test_main import test_client, clear_db, app, override_check_auth
from src.tests.test_utils import add_test_ticket_to_db, get_comment_by_id, get_first_comment

def test_add_comment(clear_db):
    added_ticket_one = add_test_ticket_to_db(title="title-1")
    response = test_client.post(
        "/tickets/comment/"+added_ticket_one.id,
        json={"content": "This is a test comment."},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    comment = data["comment"]
    assert data["detail"] == "Succesfully added comment."
    assert comment["ticket_id"] == added_ticket_one.id
    assert comment["content"] == "This is a test comment."
    assert comment["author_id"] == 0 
    assert datetime.fromisoformat(comment["creation_datetime"]) <= datetime.utcnow()

def test_add_comment_invalid(clear_db):
    response = test_client.post(
        "/tickets/comment/-1",
        json={"content": "This is a test comment that refers to an invalid id."},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Ticket with id: -1 not found."
    assert get_comment_by_id("-1") == None 
    assert get_first_comment() == None

def test_add_comment_invalid_one(clear_db):
    response = test_client.post(
        "/tickets/comment/-1",
        json={},
    )
    assert response.status_code == 422, response.text
    assert get_first_comment() == None

def test_add_comment_unauthorised(clear_db):
    app.dependency_overrides.pop(check_auth, None)
    response = test_client.post(
        "/tickets/comment/-1",
        json={"content": "This is a test comment made by an unauthorised user."},
    )
    app.dependency_overrides[check_auth] = override_check_auth
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorized" 
    assert get_first_comment() == None