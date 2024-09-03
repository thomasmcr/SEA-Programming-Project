

from src.tests.test_main import test_client, clear_db, app, override_check_auth
from src.tests.test_utils import add_test_user_to_db, get_ticket_by_id, are_objects_equal, get_user_by_id
from src.dependencies.auth_dependencies import check_auth

def test_delete_user_valid(clear_db):
    added_user = add_test_user_to_db()
    response = test_client.delete(
        f'/users/{added_user.id}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user = data["user"]
    assert data["detail"] == "Succesfully deleted user."
    assert user["id"] == added_user.id
    assert get_user_by_id(added_user.id) == None

def test_delete_user_invalid(clear_db):
    user_id = -1
    response = test_client.delete(
        f'/users/{user_id}'
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f'User with id: {user_id} not found.'

def test_delete_user_unauthorised(clear_db):
    app.dependency_overrides.pop(check_auth, None) #Remove auth override 
    added_user = add_test_user_to_db()
    response = test_client.delete(
        f'/users/{added_user.id}'
    )
    app.dependency_overrides[check_auth] = override_check_auth
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorized"
    assert are_objects_equal(added_user, get_user_by_id(added_user.id)) == True

def test_delete_priveliged_user(clear_db):
    added_user = add_test_user_to_db(is_admin=True)
    response = test_client.delete(
        f'/users/{added_user.id}'
    )
    app.dependency_overrides[check_auth] = override_check_auth
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == f'User with id: {0} is not authorised to delete user with id: {added_user.id}.'
    assert are_objects_equal(added_user, get_user_by_id(added_user.id)) == True
 
    