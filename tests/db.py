from werkzeug.security import generate_password_hash
from database.manager import DBManager
from database.schemas import UserSchema, ItemSchema, AddressSchema, OrderSchema
import tests.config as test_config
import copy


def create_dummy_user(user_payload: dict, address_payload: dict) -> int:
    session = DBManager().session()

    address = AddressSchema(**address_payload)

    test_user: dict = copy.deepcopy(user_payload)
    test_user["password"] = generate_password_hash(test_user.get("password"))
    user = UserSchema(**test_user)
    user_id = copy.copy(user.iduser)

    session.add(address)
    session.add(user)
    session.commit()
    session.close()
    return user_id


def delete_dummy_user(user_payload: dict, address_payload: dict) -> int:
    session = DBManager().session()

    session.query(OrderSchema).filter(user_payload.get("iduser") == OrderSchema.user_id).delete()
    session.query(UserSchema).filter(user_payload.get("iduser") == UserSchema.iduser).delete()
    session.query(AddressSchema).filter(address_payload.get("idaddress") == AddressSchema.idaddress).delete()

    session.commit()
    session.close()
    return user_payload.get("iduser")


def init_dummy_user(user_payload: dict = test_config.TEST_USER, address_payload: dict = test_config.TEST_ADDRESS):
    delete_dummy_user(user_payload, address_payload)
    create_dummy_user(user_payload, address_payload)


def delete_user(user_id: int):
    session = DBManager().session()
    session.query(OrderSchema).filter(user_id == OrderSchema.user_id).delete()
    session.query(UserSchema).filter(user_id == UserSchema.iduser).delete()
    session.commit()
    session.close()
    return user_id


def create_dummy_item(item_payload: dict) -> int:
    session = DBManager().session()
    item = ItemSchema(**item_payload)
    session.add(item)
    session.commit()
    session.close()
    return item_payload.get("iditem")


def delete_dummy_item(item_payload: dict) -> int:
    session = DBManager().session()
    session.query(OrderSchema).filter(item_payload.get("iditem") == OrderSchema.item_id).delete()
    session.query(ItemSchema).filter(item_payload.get("iditem") == ItemSchema.iditem).delete()
    session.commit()
    session.close()
    return item_payload.get("iditem")


def init_dummy_item(item_payload: dict = test_config.TEST_ITEM):
    delete_dummy_item(item_payload)
    create_dummy_item(item_payload)


def delete_item(item_id: int):
    session = DBManager().session()
    session.query(OrderSchema).filter(item_id == OrderSchema.item_id).delete()
    session.query(ItemSchema).filter(item_id == ItemSchema.iditem).delete()
    session.commit()
    session.close()
    return item_id


def create_dummy_order(order_payload: dict = test_config.TEST_ORDER) -> int:
    session = DBManager().session()
    order = OrderSchema(**order_payload)
    session.add(order)
    session.commit()
    session.close()
    return order_payload.get("idorder")


def delete_dummy_order(order_payload: dict) -> int:
    session = DBManager().session()
    session.query(OrderSchema).filter(order_payload.get("idorder") == OrderSchema.idorder).delete()
    session.commit()
    session.close()
    return order_payload.get("idorder")


def init_dummy_order(order_payload: dict = test_config.TEST_ORDER):
    delete_dummy_order(order_payload)
    create_dummy_order(order_payload)


def delete_order(order_id: int):
    session = DBManager().session()
    session.query(OrderSchema).filter(order_id == OrderSchema.idorder).delete()
    session.commit()
    session.close()
    return order_id
