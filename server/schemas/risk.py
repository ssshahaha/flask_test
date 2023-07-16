from marshmallow import Schema, fields, post_dump, post_load

from schemas.base import BaseSchema


class RiskBaseSchema(Schema):
    device_serial_no = fields.Str(required=True)
    target = fields.Int(required=True)
    category = fields.Int(required=True)
    value = fields.Float(missing=0.0)
    limit_value = fields.Float(missing=0.0)
    is_handled = fields.Bool(missing=False)
    risk_id = fields.Str(required=True)
    message = fields.Str(missing='')


class RiskSchema(RiskBaseSchema, BaseSchema):
    pass


class WsRiskSchema(RiskBaseSchema):
    # target_map = {0: 'device', 1: 'camera'}
    category_map = {0: '低温预警', 1: '高温预警', 2: '内存占用异常预警', 3: '磁盘占用异常预警', 4: '设备状态异常异常预警'}

    #
    # @post_load
    # def convert_data(self, data, **kwargs):
    #     for field in ['target', 'category']:
    #         field_map = self.__getattribute__(field + '_map')
    #         if data[field] not in field_map:
    #             data[field] = 'undefined'
    #         else:
    #             data[field] = field_map[data[field]]
    #     return data
    @post_load
    def make_message(self, data, **kwargs):
        target_message = "主机" if data['target'] == 0 else "相机"
        body_message = str(self.category_map.get(data['category']))
        foot_message = ""
        if data['category'] in (0, 1):
            foot_message = f"，温度为{data['value']}℃，阈值为{data['limit_value']}℃"
        elif data['category'] == 2:
            foot_message = f"，内存空间已占用{data['value']}%，阈值为{data['limit_value']}%"
        elif data['category'] == 3:
            foot_message = f"，磁盘空间已占用{data['value']}%，阈值为{data['limit_value']}%"
        elif data['category'] == 4:
            foot_message = ""
        data['message'] = target_message + body_message + foot_message
        return data


class WsUpdateRiskSchema(Schema):
    is_handled = fields.Bool(missing=False)
    risk_id = fields.Str(required=True)
