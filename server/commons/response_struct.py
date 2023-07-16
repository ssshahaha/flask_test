import json
import uuid

from flask import jsonify
from enum import Enum


class ResponseCode(Enum):
    Success = (0, 'success')
    ERROR_SYSTEM = (10000, 'Service exception')
    ERROR_CONTENT_TYPE = (10001, 'Request data is not in JSON format')
    ERROR_CAPTCHA = (10002, '验证码错误')
    ERROR_NO_USER = (10003, '用户不存在')
    ERROR_PASSWORD = (10004, '密码错误')
    ERROR_PATH_PARAM = (10005, '路径参数异常')
    ERROR_NO_DEVICE = (10006, '未找到设备')
    ERROR_MISS_PARAM = (10007, '缺少参数')
    ERROR_DEVICE_OFFLINE = (10008, '设备离线')
    # ERROR_AUTH = (6000, 'Insufficient permission, access forbidden')
    # ERROR_NO_LOGIN = (6001, 'Login status failure')
    # ERROR_PHOTO = (8001, 'Abnormal photographing')
    # ERROR_DETECT = (8002, 'Abnormal detection')
    # ERROR_SYSTEM = (8003, 'Service exception')
    # ERROR_PARAMS = (8004, 'Request parameter exception')
    # ERROR_NO_DETECT_TASK = (8006, 'No detect task')
    # ERROR_NO_DETECT_Record = (8007, 'No detect record')

    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[-1]


def api_response(code=0, message='success', data=None, json_encoder=None):
    if data is None:
        data = {}
    request_id = uuid.uuid4().hex
    if json_encoder:
        data = json.loads(json.dumps(data, cls=json_encoder))
    return jsonify({'code': code, 'message': message, 'data': data, 'request_id': request_id})


def predefined_response(response_code):
    return api_response(code=response_code.code, message=response_code.message)
