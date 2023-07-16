from marshmallow import Schema, fields


class BaseSchema(Schema):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(as_string=True, required=True, format='%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime(as_string=True, required=True, format='%Y-%m-%d %H:%M:%S')
