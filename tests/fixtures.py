from api.routes import app
import tests.config as test_config
import tests.db as test_db

import datetime
import pytest


@pytest.fixture(scope="session", autouse=True)
def init():
    """
    This function is executed before the actual tests
    to initialize test database records.
    :return: None
    """
    test_db.init_dummy_user()
    test_db.init_dummy_user(user_payload=test_config.TEST_VICTIM_USER, address_payload=test_config.TEST_VICTIM_ADDRESS)
    test_db.init_dummy_user(user_payload=test_config.TEST_ADMIN_USER, address_payload=test_config.TEST_ADMIN_ADDRESS)

    test_db.init_dummy_item()
    test_db.init_dummy_order()


@pytest.fixture()
def app_fixture():
    new_app = app
    new_app.config['TESTING'] = True

    with new_app.app_context():
        with new_app.test_client() as client:
            yield client


@pytest.fixture()
def user_json_fixture():
    return {
        "username": test_config.TEST_USER.get("username"),
        "firstname": test_config.TEST_USER.get("firstname"),
        "lastname": test_config.TEST_USER.get("lastname"),
        "email": test_config.TEST_USER.get("email"),
        "password": test_config.TEST_USER.get("password"),
        "phone": test_config.TEST_USER.get("phone"),
        "address_id": test_config.TEST_USER.get("address_id")
    }


@pytest.fixture()
def user_id_fixture():
    return test_config.TEST_USER.get("iduser")


@pytest.fixture()
def user_credentails_fixture() -> tuple:
    username, password = test_config.TEST_USER.get("username"), test_config.TEST_USER.get("password")
    return username, password


@pytest.fixture()
def admin_credentails_fixture() -> tuple:
    username, password = test_config.TEST_ADMIN_USER.get("username"), test_config.TEST_ADMIN_USER.get("password")
    return username, password


@pytest.fixture()
def user_invalid_credentails_fixture() -> tuple:
    return "yooooooooo", "looo"


@pytest.fixture()
def item_json_fixture():
    return {
        "name": test_config.TEST_ITEM.get("name"),
        "amount": test_config.TEST_ITEM.get("amount"),
        "price": test_config.TEST_ITEM.get("price"),
        "category": test_config.TEST_ITEM.get("category"),
        "status": test_config.TEST_ITEM.get("status")
    }


@pytest.fixture()
def item_id_fixture():
    return test_config.TEST_ITEM.get("iditem")


@pytest.fixture()
def order_json_fixture():
    return {
        "orderDate": datetime.datetime.now(),
        "payment_method": test_config.TEST_ORDER.get("payment_method"),
        "quantity": test_config.TEST_ORDER.get("quantity"),
        "status": test_config.TEST_ORDER.get("status"),
        "user_id": test_config.TEST_ORDER.get("user_id"),
        "item_id": test_config.TEST_ORDER.get("item_id")
    }


@pytest.fixture()
def order_id_fixture():
    return test_config.TEST_ORDER.get("idorder")
