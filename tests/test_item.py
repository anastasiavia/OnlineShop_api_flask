from unittest.mock import ANY
import tests.db as test_db
from tests.fixtures import *


def test_valid_item_creation(app_fixture, item_json_fixture, admin_credentails_fixture):
    response = app_fixture.post(
        f"/item",
        json=item_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert response.json.get("itemId") == ANY

    test_db.delete_item(item_id=response.json.get("itemId"))


def test_invalid_item_creation(app_fixture, item_json_fixture, admin_credentails_fixture):
    item_json_fixture["name"] = 12  # Invalid type.
    response = app_fixture.post(
        f"/item",
        json=item_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400
    assert response.json.get("message") == ANY


def test_valid_item_update(app_fixture, item_id_fixture, item_json_fixture, admin_credentails_fixture):
    response = app_fixture.put(
        f"/item/{item_id_fixture}",
        json=item_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert response.json.get("itemId") == ANY


def test_invalid_item_update(app_fixture, item_id_fixture, item_json_fixture, admin_credentails_fixture):
    # Test item that does not exist.
    response = app_fixture.put(
        f"/item/{100000}",
        json=item_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400

    # Test invalid json data.
    item_json_fixture["name"] = 12  # Invalid type.
    response = app_fixture.put(
        f"/item/{item_id_fixture}",
        json=item_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400


def test_get_valid_item(app_fixture, item_id_fixture, admin_credentails_fixture):
    response = app_fixture.get(
        f"/item/{item_id_fixture}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert response.json.get("name") == ANY


def test_get_invalid_item(app_fixture, item_id_fixture, admin_credentails_fixture):
    response = app_fixture.get(
        f"/item/{100000}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400


def test_delete_valid_item(app_fixture, item_id_fixture, admin_credentails_fixture):
    response = app_fixture.delete(
        f"/item/{item_id_fixture}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert response.json.get("itemId") == ANY

    test_db.init_dummy_item()


def test_delete_invalid_item(app_fixture, item_id_fixture, admin_credentails_fixture):
    response = app_fixture.delete(
        f"/item/{100000}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400