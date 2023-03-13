from flask import make_response, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from typing import Union

from database.schemas import UserSchema
import database.crud as db


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    if user and check_password_hash(user.password, password):
        return username
    return False


def require_role():
    def decoration(func):

        def inner(*args, **kwargs):
            user: UserSchema = db.get_user(query_id=auth.get_auth().username, by=UserSchema.username)
            if not user or not user.is_admin:
                return make_response({"message": "Unauthorized Access"}, 401)
            return func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner
    return decoration


def get_current_user() -> UserSchema:
    username = auth.current_user()
    user: UserSchema = db.get_user(query_id=username, by=UserSchema.username)
    return user


def validate_user(user_id) -> Union[Response, None]:
    if get_current_user().iduser != user_id:
        response = {
           "code": 401,
           "message": "Unauthorized user access"
        }
        return make_response(response, 401)
    return None
