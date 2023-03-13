from unittest.mock import ANY
import tests.config as test_config
import tests.db as test_db
from tests.fixtures import *


def test_valid_user_creation(app_fixture, user_json_fixture):
    response = app_fixture.post("/user", json=user_json_fixture)

    assert response.status_code == 200
    assert response.json == {"userId": ANY}

    test_db.delete_user(user_id=response.json.get("userId"))


def test_invalid_user_creation(app_fixture, user_json_fixture):
    user_json_fixture["username"] = 12  # Invalid type. Has to be str.
    response = app_fixture.post("/user", json=user_json_fixture)

    assert response.status_code == 400
    assert response.json == {
        "code": 400,
        "message": ANY
    }

    user_json_fixture["address_id"] = 9999  # Such address does not exist.
    response = app_fixture.post("/user", json=user_json_fixture)

    assert response.status_code == 400
    assert response.json == {
        "code": 400,
        "message": ANY
    }


def test_valid_login(app_fixture, user_credentails_fixture):
    response = app_fixture.get(
        "/user/login",
        auth=user_credentails_fixture
    )

    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_invalid_login(app_fixture, user_credentails_fixture, user_invalid_credentails_fixture):
    # Test invalid user.
    response = app_fixture.get(
        "/user/login",
        auth=user_invalid_credentails_fixture
    )
    assert response.status_code == 400

    # Test invalid password of existing user.
    response = app_fixture.get(
        "/user/login",
        auth=(user_credentails_fixture[0], "")
    )
    assert response.status_code == 401


def test_get_user_by_username(app_fixture, user_credentails_fixture):
    # Test invalid user.
    response = app_fixture.get(
        f"/user/{user_credentails_fixture[0]}",
        auth=user_credentails_fixture,
    )
    assert response.status_code == 200
    assert response.json.get("username") == user_credentails_fixture[0]


def test_get_user_by_invalid_username(app_fixture, user_invalid_credentails_fixture):
    # Test invalid user.
    response = app_fixture.get(
        f"/user/{user_invalid_credentails_fixture[0]}",
        auth=user_invalid_credentails_fixture,
    )
    assert response.status_code == 401


def test_user_logout(app_fixture, user_credentails_fixture):
    # Test invalid user.
    response = app_fixture.get(
        "/user/logout",
        auth=user_credentails_fixture,
    )
    assert response.status_code == 200


def test_update_valid_user(app_fixture, user_id_fixture, user_json_fixture, user_credentails_fixture):
    # Test invalid user.
    response = app_fixture.put(
        f"/user/{user_id_fixture}",
        auth=user_credentails_fixture,
        json=user_json_fixture
    )
    assert response.status_code == 200
    assert response.json.get("userId") == user_id_fixture


def test_update_invalid_user(app_fixture, user_id_fixture, user_json_fixture, user_credentails_fixture):
    # Test user that does not exist.
    response = app_fixture.put(
        f"/user/{100000}",
        auth=user_credentails_fixture,
        json=user_json_fixture
    )
    assert response.status_code == 400
    assert response.json.get("message") == "There is no such id in database"

    # Test not logged-in user.
    response = app_fixture.put(
        f"/user/{test_config.TEST_VICTIM_USER.get('iduser')}",
        auth=user_credentails_fixture,
        json=user_json_fixture
    )
    assert response.status_code == 401

    # Test validation error
    user_json_fixture["username"] = 12  # Invalid type. Has to be str.
    response = app_fixture.put(
        f"/user/{user_id_fixture}",
        auth=user_credentails_fixture,
        json=user_json_fixture
    )
    assert response.status_code == 400


def test_delete_valid_user(app_fixture, user_id_fixture, user_credentails_fixture):
    response = app_fixture.delete(
        f"/user/{user_id_fixture}",
        auth=user_credentails_fixture
    )
    assert response.status_code == 200
    assert response.json.get("userId") == user_id_fixture

    test_db.init_dummy_user()


def test_get_all_users(app_fixture, admin_credentails_fixture):
    response = app_fixture.get(
        f"/users",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert isinstance(response.json.get("users"), list)
