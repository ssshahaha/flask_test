from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE, validates

from schemas.base import BaseSchema


class DetectionBaseSchema(Schema):
    device_serial_no = fields.Str(required=True)
    detection_id = fields.Str(data_key='id')
    detection_create_time = fields.Str(data_key='create_time')
    detection_update_time = fields.Str(data_key='update_time')
    report_code = fields.Int(required=True)
    x = fields.Int(required=True)
    y = fields.Int(required=True)
    z = fields.Int(required=True)
    angle = fields.Float(missing=0.0)
    depths = fields.Str(required=True)
    spent_ms = fields.Int(required=True)
    image_path = fields.Str(missing='', allow_none=True, default='')
    # result = fields.Str(required=True)
    request_address = fields.Int(required=True)
    plc_work_flow = fields.Int(required=True)
    detection_type = fields.Str(required=True)  # plc,api


class DetectionSchema(DetectionBaseSchema, BaseSchema):
    detection_id = fields.Str(missing='')
    detection_create_time = fields.Str(missing='')
    detection_update_time = fields.Str(missing='')

    @post_dump
    def convert_data(self, data, **kwargs):
        if data.get('image_path'):
            image_name = data.get('image_path').split('/')[-1].split('\\')[-1]
            data['cloud_image_name'] = data.get('detection_id', '') + '_' + image_name
        else:
            data['cloud_image_name'] = ''
        return data


class WsDetectionSchema(Schema):
    device_serial_no = fields.Str(required=True)
    # detection_type = fields.Str(required=True)  # plc,api
    detection_data = fields.Nested(DetectionBaseSchema, many=True, unknown=EXCLUDE)
    upload_time = fields.Str(required=True)
