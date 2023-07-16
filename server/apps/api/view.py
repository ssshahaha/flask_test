from flask import request
from loguru import logger

from . import api
from commons.response_struct import api_response, ResponseCode, predefined_response

logger = logger.bind(name='app')


@api.before_request
def api_before_request():
    if request.method == 'POST' and (not request.content_type or 'application/json' not in request.content_type):
        return predefined_response(ResponseCode.ERROR_CONTENT_TYPE)


@api.errorhandler(Exception)
def api_errorhandler(e):
    logger.error(f'api_errorhandler:{e}')
    return api_response(code=ResponseCode.ERROR_SYSTEM.code, message=ResponseCode.ERROR_SYSTEM.message,
                        data={'error_detail': '{}'.format(e)})


@api.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        from crud import crud_device_message
        # db = get_db().next()
        print(crud_device_message.get('test'))
        return api_response(data={'data': 'test'})
    if request.method == 'POST':
        # request_data = request.get_json()
        from schemas.device_message import DeviceMessageBaseSchema
        schema = DeviceMessageBaseSchema()
        device_message_data = schema.loads(request.get_data(as_text=True))
        print(device_message_data, type(device_message_data))
        from crud import crud_device_message
        crud_device_message.create(device_message_data)
        return api_response()


@api.route('/statistics', methods=['POST'])
def statistics():
    request_data = request.get_json()
    return api_response(data=request_data)
