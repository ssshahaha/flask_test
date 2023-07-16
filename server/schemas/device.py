import json

from marshmallow import Schema, fields, post_dump

from schemas.base import BaseSchema


class DeviceBaseSchema(Schema):
    device_name = fields.Str(missing='')
    device_address = fields.Str(missing='')
    station_name = fields.Str(missing='')
    device_serial_no = fields.Str(required=True)
    device_customer = fields.Str(missing='')
    app_version = fields.Str(missing='')
    model_version = fields.Str(missing='')
    device_config = fields.Str(missing='{}')
    device_risk_status = fields.Bool(missing=False)
    camera_risk_status = fields.Bool(missing=False)


class DeviceSchema(DeviceBaseSchema, BaseSchema):
    online_status = fields.Bool(missing=False)

    @post_dump
    def convert_device_config(self, data, **kwargs):
        if data:
            if not data['device_config']:
                data['device_config'] = {}
            else:
                try:
                    data['device_config'] = json.loads(data['device_config'])
                except:
                    data['device_config'] = {}
        return data


class UpdateDeviceSchema(DeviceBaseSchema):
    id = fields.Integer(required=True)
    updated_at = fields.DateTime(as_string=True, required=True)
    is_delete = fields.Boolean(required=True)
    online_status = fields.Bool(missing=False)
