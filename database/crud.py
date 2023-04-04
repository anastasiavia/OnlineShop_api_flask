from werkzeug.security import generate_password_hash
from database.manager import DBManager
from database.schemas import UserSchema, ItemSchema, OrderSchema
from typing import Union

import random
import datetime
import sqlalchemy


session = DBManager().session()


# def create_address(street: str, city: str, house_number: int) -> int:
#     address = AddressSchema(
#         idaddress=random.randint(1, 10000),
#         street=street,
#         city=city,
#         house_number=house_number
#     )
#     session.add(address)
#     session.commit()
#     return address.idaddress


def get_user(query_id: Union[int, str], by=UserSchema.iduser) -> UserSchema:
    record = session.query(UserSchema).filter(by == query_id).first()
    return record


def create_user(
        username: str, firstname: str, lastname: str, email: str,
        password: str, phone: str, is_admin: bool = False
) -> int:
    password_hash = generate_password_hash(password)
    user = UserSchema(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password_hash,
        phone=phone,
        is_admin=is_admin
    )
    session.add(user)
    session.commit()
    return user.iduser


def update_user(
    user_id: int, username: str, firstname: str, lastname: str, email: str, password: str, phone: str, address_id: int
) -> int:
    password_hash = generate_password_hash(password)
    new_user = {
        'username': username,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'password': password_hash,
        'phone': phone,
        'address_id': address_id
    }
    session.query(UserSchema).filter(user_id == UserSchema.iduser).update(new_user)
    session.commit()
    return user_id



def delete_user(user_id: int) -> int:

    session.query(UserSchema).filter(user_id == UserSchema.iduser).delete()
    session.commit()
    return user_id


def create_item(name: str, amount: int, price: int, category: str, status: str, description: str, image: str) -> int:
    item = ItemSchema(
        name=name,
        amount=amount,
        price=price,
        category=category,
        status=status,
        description=description,
        image=image

    )
    session.add(item)
    session.commit()
    return item.iditem


def get_item(query_id: Union[int, str], by=ItemSchema.iditem) -> ItemSchema:
    record = session.query(ItemSchema).filter(by == query_id).first()
    return record


def update_item(item_id: int, payload: dict) -> int:
    session.query(ItemSchema).filter(item_id == ItemSchema.iditem).update(payload)
    session.commit()
    return item_id


def delete_item(item_id: int, item_record: ItemSchema) -> int:
    session.delete(item_record)
    session.commit()
    return item_id


def create_order(quantity: int, address: str, cost: int, message: str, user_id: int, item_id: int) -> int:
    order_record = OrderSchema(
        quantity=quantity,
        address=address,
        cost=cost,
        message=message,
        user_id=user_id,
        item_id=item_id,

    )
    session.add(order_record)
    session.commit()
    return order_record.idorder


def get_order(query_id: Union[int, str], by=OrderSchema.idorder) -> OrderSchema:
    record = session.query(OrderSchema).filter(by == query_id).first()
    return record


def delete_order(order_id: int, order_record: OrderSchema) -> int:
    session.delete(order_record)
    session.commit()
    return order_id


def get_all_users() -> list:
    users = session.execute(sqlalchemy.select(UserSchema))
    users = users.scalars().all()
    users = [user.as_dict() for user in users]
    return users


def get_store_inventory() -> list:
    items = session.execute(sqlalchemy.select(ItemSchema))
    items = items.scalars().all()
    items = [item.as_dict() for item in items]
    return items
