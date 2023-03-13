from marshmallow import Schema, fields, validate


class UserCreation(Schema):
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    email = fields.String()
    password = fields.String()
    phone = fields.String()
    address_id = fields.Integer()


class ItemCreation(Schema):
    name = fields.String()
    amount = fields.Integer(validate=[validate.Range(min=0, min_inclusive=True, error="Amount can`t be 0<")])
    price = fields.Integer(validate=[validate.Range(min=0, min_inclusive=True, error="Price can`t be 0<")])
    category = fields.String()
    status = fields.String()


class OrderCreation(Schema):
    quantity = fields.Integer()
    orderDate = fields.String()
    status = fields.String()
    payment_method = fields.String()
    user_id = fields.Integer()
    item_id = fields.Integer()
