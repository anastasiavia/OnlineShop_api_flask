import datetime


from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from werkzeug.security import check_password_hash
from marshmallow.exceptions import ValidationError
from flask import Flask, request, make_response, jsonify

from schemas import UserCreation, ItemCreation, OrderCreation
from auth import auth, validate_user, require_role
from database.schemas import UserSchema
import database.crud as db
from flask_cors import CORS
import sqlalchemy.exc as sql_exception



app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'd5fb8c4fa8bd46638dadc4e751e0d68d'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=4)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
CORS(app)

blacklist = set()
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(some, decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


def check_if_token_is_revoked(some, token):
    jti = token["jti"]
    token_in_redis = blacklist.get(jti)
    return token_in_redis is not None


@app.route('/user', methods=['POST'])
def post_user():
    try:
        user: dict = UserCreation().load(request.get_json())
        user_id = db.create_user(
            username=user.get("username"), firstname=user.get("firstname"), lastname=user.get("lastname"),
            email=user.get("email"), password=user.get("password"),
            phone=user.get("phone")
        )
    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)
    response = make_response({"userId": user_id}, 200)
    return response


@app.route('/user/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")



    # request_auth = request.authorization
    # username, password = request_auth.username, request_auth.password

    if not auth or not username or not password:
        response = {
            "code": 401,
            "message": "Username of password is invalid."
        }
        return make_response(response, 401)

    user: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    if user and check_password_hash(user.password, password):
        resp = jsonify(success=True)
        resp.status_code = 200
        token = create_access_token("common_user")
        return {'token': token.decode('utf-8')}
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
# @auth.login_required
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
@jwt_required()

def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return "Logout successful"


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
# @auth.login_required
# @require_role()
def post_item():
    request_json = request.get_json()

    try:
        item = ItemCreation().load(request_json)
        item_id = db.create_item(
            name=item.get("name"), amount=item.get("amount"), price=item.get("price"),
            category=item.get("category"), status=item.get("status"), description=item.get("description"), image=item.get("image")
        )
    except ValidationError as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)
    respose = make_response({"itemId": item_id}, 200)
    return respose
# def post_item():
#     request_json = request.form.to_dict()
#     try:
#         item = ItemCreation().load(request_json)
#         photo_file = request.files.get('photo')
#         photo_path = save_photo(photo_file)
#         item_id = db.create_item(
#             name=item.get("name"), amount=item.get("amount"), price=item.get("price"),
#             category=item.get("category"), status=item.get("status"), image=photo_path
#         )
#     except ValidationError as e:
#         response = {
#             "code": 400,
#             "message": f"Server crashed with the following error: {str(e)}"
#         }
#         return make_response(response, 400)
#     response = make_response({"itemId": item_id}, 200)
#     return response


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
# @auth.login_required
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
@jwt_required()
def post_order():
    request_json = request.get_json()
    try:
        # validate request input
        order = OrderCreation().load(request_json)
        print(order)

        # create database record
        order_id = db.create_order(
            quantity=order.get('quantity'), address=order.get('address'), cost=order.get('cost'), message=order.get('message'),
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
    return make_response(db.get_store_inventory(), 200)


if __name__ == '__main__':
    app.run(port=5000)
