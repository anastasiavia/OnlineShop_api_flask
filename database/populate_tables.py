# import database.crud as db
#
#
# if __name__ == '__main__':
#     item_id_1 = db.create_item(name="notepad", amount=8, price=300, status="available", category="uni stuff")
#     item_id_2 = db.create_item(name="pencil", amount=8, price=300, status="available", category="uni stuff")
#
#     address_id_1 = db.create_address(street="Kulparkivska", city="Lviv", house_number=95)
#     address_id_2 = db.create_address(street="Korolenka", city="Lviv", house_number=1)
#
#     user_id_1 = db.create_user(
#         username="Admin", firstname="Admin", lastname="Admin", email="admin@gmail.com",
#         password="pass", phone="+38(096)-565-8519", is_admin=True
#     )
#     user_id_2 = db.create_user(
#         username="User1", firstname="User1", lastname="User1", email="User1@gmail.com",
#         password="pass", phone="+38(096)-565-8519"
#     )
#
#     order_id_1 = db.create_order(
#         quantity=6, status="packed", payment_method="later", user_id=user_id_1, item_id=item_id_1
#     )
#     order_id_2 = db.create_order(
#         quantity=8, status="packed", payment_method="later", user_id=user_id_2, item_id=item_id_2
#     )
