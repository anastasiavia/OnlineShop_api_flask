import datetime


TEST_ADDRESS = {
    "idaddress": 1003,
    "street": "Test",
    "city": "Test",
    "house_number": 1000
}

TEST_USER = {
    "iduser": 1003,
    "username": 'test_dummy_user',
    "firstname": "test",
    "lastname": "test",
    "email": "test@gmail.com",
    "password": 'pass',
    "phone": "12345",
    "address_id": TEST_ADDRESS.get("idaddress"),
    "is_admin": False
}

TEST_VICTIM_ADDRESS = {
    "idaddress": 1004,
    "street": "Test",
    "city": "Test",
    "house_number": 1000
}

TEST_VICTIM_USER = {
    "iduser": 1004,
    "username": 'test_victim_user',
    "firstname": "test",
    "lastname": "test",
    "email": "test@gmail.com",
    "password": 'pass',
    "phone": "12345",
    "address_id": TEST_VICTIM_ADDRESS.get("idaddress"),
    "is_admin": False
}

TEST_ADMIN_ADDRESS = {
    "idaddress": 1005,
    "street": "Test",
    "city": "Test",
    "house_number": 1000
}

TEST_ADMIN_USER = {
    "iduser": 1005,
    "username": 'test_admin_user',
    "firstname": "test",
    "lastname": "test",
    "email": "test@gmail.com",
    "password": 'pass',
    "phone": "12345",
    "address_id": TEST_ADMIN_ADDRESS.get("idaddress"),
    "is_admin": True
}

TEST_ITEM = {
    "iditem": 1000,
    "name": "test_item",
    "amount": 10,
    "price": 10000,
    "category": "string",
    "status": "available"
}

TEST_ORDER = {
    "idorder": 1000,
    "quantity": 10,
    "orderDate": datetime.datetime.now(),
    "status": "test_status",
    "payment_method": "test_method",
    "user_id": TEST_ADMIN_USER.get("iduser"),
    "item_id": TEST_ITEM.get("iditem")
}
