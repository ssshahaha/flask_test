from marshmallow import Schema, fields

from schemas.base import BaseSchema


class UserBaseSchema(Schema):
    user_name = fields.Str()


class CreateUserSchema(UserBaseSchema):
    password = fields.Str()


class UpdateUserSchema(UserBaseSchema):
    password = fields.Str()
    updated_at = fields.DateTime(as_string=True, required=True)
    is_delete = fields.Boolean(required=True)


class UserDetailSchema(UserBaseSchema, BaseSchema):
    is_delete = fields.Boolean(required=True)
    password = fields.Str()
