from werkzeug.security import check_password_hash
from marshmallow.exceptions import ValidationError
from flask import Flask, request, make_response

from api.schemas import UserCreation, ItemCreation, OrderCreation
from api.auth import auth, validate_user, require_role
from database.schemas import UserSchema
import database.crud as db

import sqlalchemy.exc as sql_exception


app = Flask(__name__)


@app.route('/user', methods=['POST'])
def post_user():
    try:
        user: dict = UserCreation().load(request.get_json())
        user_id = db.create_user(
            username=user.get("username"), firstname=user.get("firstname"), lastname=user.get("lastname"),
            email=user.get("email"), password=user.get("password"),
            phone=user.get("phone"), address_id=user.get("address_id")
        )
    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)
    response = make_response({"userId": user_id}, 200)
    return response


@app.route('/user/login', methods=['GET'])
def login():
    request_auth = request.authorization
    username, password = request_auth.username, request_auth.password

    if not auth or not username or not password:
        response = {
            "code": 401,
            "message": "Username of password is invalid."
        }
        return make_response(response, 401)

    user: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    if user and check_password_hash(user.password, password):
        return UserCreation().dump(user)
    else:
        response = {
            "code": 400,
            "message": "Username of password is invalid."
        }
        return make_response(response, 400)


@app.route('/users', methods=['GET'])
@require_role()
@auth.login_required
def get_all_users():
    return make_response({"users": db.get_all_users()}, 200)


@app.route('/user/<string:username>', methods=['GET'])
@auth.login_required
def get_user_by_usernames(username):
    user_record: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    if not user_record:
        response = {
            "code": 400,
            "message": "There is no such user in database"
        }
        return make_response(response, 400)
    respose = make_response(user_record.as_dict(), 200)
    return respose



@app.route('/user/logout', methods=['GET'])
@auth.login_required
def logout():
    return make_response({"message": "Successfully logged out"}, 200)


@app.route('/user/<int:iduser>', methods=['PUT'])
@auth.login_required
def update_user(iduser):
    request_json = request.get_json()

    user_record: UserSchema = db.get_user(iduser)
    if not user_record:
        response = {
            "code": 400,
            "message": "There is no such id in database"
        }
        return make_response(response, 400)

    response = validate_user(user_id=user_record.iduser)
    if response:
        return response

    try:
        # validate request input
        user = UserCreation().load(request_json)
        user_id = db.update_user(
            user_id=iduser, username=user.get("username"), firstname=user.get("firstname"),
            lastname=user.get("lastname"), email=user.get("email"), password=user.get("password"),
            phone=user.get("phone"), address_id=user.get("address_id")
        )
    except ValidationError as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)

    respose = make_response({"userId": user_id}, 200)
    return respose


@app.route('/user/<int:iduser>', methods=["DELETE"])
@auth.login_required
def delete_user(iduser):
    user_record: UserSchema = db.get_user(iduser)
    if not user_record:
        response = {
            "code": 400,
            "message": "There is no such user"
        }
        return make_response(response, 400)

    response = validate_user(user_id=user_record.iduser)
    if response:
        return response

    user_id = db.delete_user(user_record.iduser)
    respose = make_response({"userId": user_id}, 200)
    return respose


@app.route('/item', methods=["POST"])
@auth.login_required
@require_role()
def post_item():
    request_json = request.get_json()

    try:
        item = ItemCreation().load(request_json)
        item_id = db.create_item(
            name=item.get("name"), amount=item.get("amount"), price=item.get("price"),
            category=item.get("category"), status=item.get("status")
        )
    except ValidationError as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)
    respose = make_response({"itemId": item_id}, 200)
    return respose


@app.route('/item/<int:iditem>', methods=['PUT'])
@auth.login_required
@require_role()
def update_item(iditem):
    request_json = request.get_json()

    item_record = db.get_item(iditem)
    if not item_record:
        response = {
            "code": 400,
            "message": "There is no such id in database"
        }
        return make_response(response, 400)

    try:
        # validate request input
        item = ItemCreation().load(request_json)
        # create database record
        item_id = db.update_item(item_id=iditem, payload=item)

    except ValidationError as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)
    respose = make_response({"itemId": item_id}, 200)
    return respose


@app.route('/item/<iditem>', methods=["GET"])
@auth.login_required
def get_item_by_id(iditem):
    item_record = db.get_item(iditem)
    if not item_record:
        response = {
            "code": 400,
            "message": "There is no such item in database"
        }
        return make_response(response, 400)
    respose = make_response(item_record.as_dict(), 200)
    return respose


@app.route('/item/<iditem>', methods=["DELETE"])
@auth.login_required
@require_role()
def delete_item(iditem):
    item_record = db.get_item(iditem)
    if not item_record:
        response = {
            "code": 400,
            "message": "There is no such item"
        }
        return make_response(response, 400)

    item_id = db.delete_item(item_id=iditem, item_record=item_record)

    respose = make_response({"itemId": item_id}, 200)
    return respose


@app.route('/store/order', methods=["POST"])
@auth.login_required
def post_order():
    request_json = request.get_json()
    try:
        # validate request input
        order = OrderCreation().load(request_json)
        print(order)

        # create database record
        order_id = db.create_order(
            quantity=order.get('quantity'), status=order.get('status'), payment_method=order.get('payment_method'),
            user_id=order.get('user_id'), item_id=order.get('item_id')
        )
        print(order_id)

    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)

    respose = make_response({"orderId": order_id}, 200)
    return respose


@app.route('/order/<int:idorder>', methods=['GET'])
@auth.login_required
@require_role()
def get_order_by_id(idorder):
    order_record = db.get_order(idorder)
    # print(get_current_user().iduser)
    # print(get_current_user().is_admin)
    if not order_record:
        response = {
            "code": 400,
            "message": "There is no such order in database"
        }
        return make_response(response, 400)

    # response = validate_admin(user_id=order_record.user_id)
    # if response:
    #     return response

    respose = make_response(order_record.as_dict(), 200)
    return respose


@app.route('/store/order/<int:idorder>', methods=["DELETE"])
@auth.login_required
@require_role()
def delete_order(idorder):
    order_record = db.get_order(idorder)
    if not order_record:
        response = {
            "code": 400,
            "message": "There is no such order"
        }
        return make_response(response, 400)

    # response = validate_admin(user_id=order_record.user_id)
    # if response:
    #     return response

    order_id = db.delete_order(order_id=idorder, order_record=order_record)

    respose = make_response({"orderId": order_id}, 200)
    return respose


@app.route('/store/inventory', methods=['GET'])
def return_inventory():
    return make_response({"inventory": db.get_store_inventory()}, 200)


if __name__ == '__main__':
    app.run(port=5000)
