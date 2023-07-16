from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE, validates

from schemas.base import BaseSchema


class ExceptionBaseSchema(Schema):
    exception_code = fields.Str(required=True)
    stage = fields.Str(required=True)
    type = fields.Str(required=True)
    prompt = fields.Str(required=True)
    reason = fields.Str(required=True)
    solution = fields.Str(required=True)
    report_code = fields.Int(required=True)
    plc_work_flow = fields.Int(required=True)


class DeviceExceptionSchema(ExceptionBaseSchema, BaseSchema):
    pass
