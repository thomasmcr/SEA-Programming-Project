from src.tests.test_main import test_client, clear_db

def test_create_ticket(clear_db):
    response = test_client.post(
        "/tickets/",
        json={"title": "Test Ticket", "content": "this is some content."},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "message" in data
    assert "ticket" in data

    message = data["message"]
    ticket = data["ticket"]

    assert message == "Succesfully added ticket."

    assert "id" in ticket
    assert "title" in ticket
    assert "content" in ticket
    assert "resolved" in ticket

    assert ticket["title"] == "Test Ticket"
    assert ticket["content"] == "this is some content."
    assert ticket["resolved"] is False