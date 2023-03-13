from unittest.mock import ANY
import tests.db as test_db
from tests.fixtures import *


def test_valid_order_creation(app_fixture, order_json_fixture, admin_credentails_fixture):
    response = app_fixture.post(
        f"/store/order",
        json=order_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert response.json.get("orderId") == ANY

    test_db.delete_order(order_id=response.json.get("orderId"))


def test_invalid_order_creation(app_fixture, order_json_fixture, admin_credentails_fixture):
    order_json_fixture["quantity"] = "hello"  # Invalid type.
    response = app_fixture.post(
        f"/store/order",
        json=order_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400
    assert response.json.get("message") == ANY

    # Test invalid foreign key.
    order_json_fixture["user_id"] = 100000  # Invalid type.
    response = app_fixture.post(
        f"/store/order",
        json=order_json_fixture,
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400
    assert response.json.get("message") == ANY


def test_get_valid_order(app_fixture, order_id_fixture, admin_credentails_fixture):
    # Init order because it may be deleted because of the foreign key in Item deletion.
    test_db.init_dummy_order()

    response = app_fixture.get(
        f"/order/{order_id_fixture}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_get_invalid_order(app_fixture, order_id_fixture, admin_credentails_fixture):
    response = app_fixture.get(
        f"/order/{10000}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400


def test_delete_valid_order(app_fixture, order_id_fixture, admin_credentails_fixture):
    # Init order because it may be deleted because of the foreign key in Item deletion.
    test_db.init_dummy_order()

    response = app_fixture.delete(
        f"/store/order/{order_id_fixture}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)

    test_db.init_dummy_order()


def test_delete_invalid_order(app_fixture, order_id_fixture, admin_credentails_fixture):
    response = app_fixture.delete(
        f"/store/order/{100000}",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 400


def test_get_store_inventory(app_fixture, admin_credentails_fixture):
    response = app_fixture.get(
        f"/store/inventory",
        auth=admin_credentails_fixture
    )
    assert response.status_code == 200
    assert isinstance(response.json.get("inventory"), list)
