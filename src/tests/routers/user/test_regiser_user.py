
from src.tests.test_main import test_client, clear_db
from src.tests.test_utils import add_test_user_to_db, get_first_user, count_users

def test_register_user(clear_db):
    response = test_client.post(
        "/users/register",
        json={"username": "username", "password": "password"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user = data["user"]
    assert data["detail"] == "Succesfully registered user."
    assert set(user.keys()) == {"id", "is_admin", "username"}
    assert user["username"] == "username"
    assert get_first_user() != None

def test_register_user_invalid_blank_body(clear_db):
    response = test_client.post(
        "/users/register",
        json={"username": "", "password": ""},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username and password cannot be blank." 
    assert get_first_user() == None

def test_register_user_invalid_username_in_use(clear_db):
    added_user = add_test_user_to_db()
    response = test_client.post(
        "/users/register",
        json={"username": "username", "password": "password"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == f"Username {added_user.username} already in use."
    assert count_users() == 1

def test_register_user_invalid_short_password(clear_db):
    response = test_client.post(
        "/users/register",
        json={"username": "username", "password": "short"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be at least 8 characters long."
    assert get_first_user() == None; 
    
    