from marshmallow import Schema, fields


class DeviceMessageBaseSchema(Schema):
    device_serial_no = fields.Str(required=True)
    last_calibrate_time = fields.Str(missing='')
    app_version = fields.Str(missing='')
    model_version = fields.Str(missing='')
    plc_connect_status = fields.Boolean(missing=True)
    camera_connect_status = fields.Boolean(missing=True)
    station_connect_status = fields.Boolean(missing=True)
    device_temperature = fields.Float(missing=0.0, allow_none=True, default=0.0)
    device_cpu_usage = fields.Float(missing=0.0, allow_none=True, default=0.0)
    device_mem_usage = fields.Float(missing=0.0, allow_none=True, default=0.0)
    device_disk_usage = fields.Float(missing=0.0, allow_none=True, default=0.0)
    camera_temperature = fields.Float(missing=0.0, allow_none=True, default=0.0)
    power_change_times = fields.Integer(missing=0)
    detect_times = fields.Integer(missing=0)
    detect_success_times = fields.Integer(missing=0)
    detect_success_rate = fields.Float(missing=0.0)
    detect_fail_times = fields.Integer(missing=0)
    detect_fail_rate = fields.Float(missing=0.0)
    risk_times = fields.Integer(missing=0)
    exception_times = fields.Integer(missing=0)
    daily_detect_times = fields.Integer(missing=0)
    week_statistics_data = fields.Str(missing='{}')


class DeviceMessageSchema(DeviceMessageBaseSchema):
    id = fields.Integer(required=True, allow_none=True)
    created_at = fields.DateTime(as_string=True, format='%Y-%m-%d %H:%M:%S', allow_none=True, missing='')
    updated_at = fields.DateTime(as_string=True, format='%Y-%m-%d %H:%M:%S', allow_none=True, missing='')
