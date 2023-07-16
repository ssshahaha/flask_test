from marshmallow import Schema, fields


class LoginSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    captcha_id = fields.Str(required=True)
    captcha_text = fields.Str(required=True)
