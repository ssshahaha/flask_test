from flask import request
from loguru import logger

from . import root
from commons.response_struct import api_response, ResponseCode

logger = logger.bind(name='app')


@root.before_request
def root_before_request():
    logger.info(f'url:{request.url} content_type:{request.content_type}')


@root.errorhandler(Exception)
def root_errorhandler(e):
    logger.error(f'root_errorhandler:{e}')
    return api_response(code=ResponseCode.ERROR_SYSTEM.code, message=ResponseCode.ERROR_SYSTEM.message,
                        data={'error_detail': '{}'.format(e)})


@root.route('/root', methods=['POST', 'GET'])
def root():
    if request.method == 'GET':
        return api_response(data={'data': 'root'})
    if request.method == 'POST':
        return api_response(data={'data': f'{request.data}'})
