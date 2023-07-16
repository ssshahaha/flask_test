from marshmallow import Schema, fields, post_load, validates, ValidationError


class QuerySchema(Schema):
    sort = fields.Str(missing='')
    page_index = fields.Int(missing=1)
    page_size = fields.Int(missing=10)
    time_range = fields.Str(missing='')
    start_time = fields.Str(missing='')
    end_time = fields.Str(missing='')

    @post_load
    def convert_query_data(self, data, **kwargs):
        data['limit'] = data['page_size']
        data['offset'] = (data['page_index'] - 1) * data['page_size']

        if data['time_range']:
            data['start_time'], data['end_time'] = data['time_range'].split(' - ')

        return data


class DeviceQuerySchema(QuerySchema):
    online_status = fields.Str(missing='all')
    device_serial_no = fields.Str(missing='')

    @validates("online_status")
    def validate_online_status(self, value):
        if value not in ['all', 'true', 'false']:
            raise ValidationError('online_status参数值异常')


class DeviceSearchSchema(Schema):
    device_serial_no = fields.Str(missing='')
    station_name = fields.Str(missing='')


class RiskQuerySchema(QuerySchema):
    is_handled = fields.Bool(missing=False)
    search = fields.Str(missing='')  # 'all':ignore query fields
    risk_target = fields.Str(missing='')
    station_name = fields.Str(missing='')
    message = fields.Str(missing='')


class StatisticsRankQuerySchema(QuerySchema):
    # target = fields.Str(missing='all')
    # top = fields.Int(missing=0)
    top = fields.Str(missing='')

    @post_load
    def convert_data(self, data, **kwargs):
        if data['top'] != '':
            data['top'] = int(data['top'])
        else:
            data['top'] = 0
        return data

    # @validates("target")
    # def validate_target(self, value):
    #     if value not in ['all', 'swap', 'risk', 'exception']:
    #         raise ValidationError('target参数值异常')


class StationQuerySchema(QuerySchema):
    station_name = fields.Str(missing='')
    device_serial_no = fields.Str(missing='')


class StationCameraPhotoSchema(QuerySchema):
    station_name = fields.Str(required=True)
    sio_id = fields.Str(required=True)


class DetectionQuerySchema(QuerySchema):
    station_name = fields.Str(missing='')
    device_serial_no = fields.Str(missing='')
