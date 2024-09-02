

from src.tests.test_main import clear_db, session
from src.tests.test_utils import add_test_user_to_db, are_objects_equal
from src.services.user_service import * 

def test_get_public_users(clear_db):

    include_users = [
        add_test_user_to_db(id=0, username="test_user_one", password="password", is_admin=False),
        add_test_user_to_db(id=1, username="test_user_two", password="password", is_admin=True)
    ]
    exclude_user = add_test_user_to_db(id=2, username="exclude_me", password="password", is_admin=False)
    db = session()
    result = get_public_users(db, [exclude_user.id])
    assert len(result) == 2

    #Check all the field keys and values are correct
    for i, public_user in enumerate(result):

        assert hasattr(public_user, "id")
        assert hasattr(public_user, "username")
        assert hasattr(public_user, "is_admin")
        assert not hasattr(public_user, "password")
        assert not hasattr(public_user, "session")

        assert public_user.id == include_users[i].id
        assert public_user.username == include_users[i].username
        assert public_user.is_admin == include_users[i].is_admin

    #Check excluded user is not in result
    assert exclude_user.id not in [user.id for user in result]
    assert exclude_user.username not in [user.username for user in result]
