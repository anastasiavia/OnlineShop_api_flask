from marshmallow import Schema, fields, validate


class UserCreation(Schema):
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    email = fields.String()
    password = fields.String()
    phone = fields.String()





class ItemCreation(Schema):
    name = fields.String()
    amount = fields.Integer(validate=[validate.Range(min=0, min_inclusive=True, error="Amount can`t be 0<")])
    price = fields.Integer(validate=[validate.Range(min=0, min_inclusive=True, error="Price can`t be 0<")])
    category = fields.String()
    status = fields.String()
    description = fields.String()
    image = fields.String()


class OrderCreation(Schema):
    quantity = fields.Integer()
    address = fields.String()
    cost = fields.Integer()
    message = fields.String()
    user_id = fields.Integer()
    item_id = fields.Integer()
