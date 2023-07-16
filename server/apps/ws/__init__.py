from engineio.payload import Payload
from flask_socketio import SocketIO, emit

Payload.max_decode_packets = 50
socket_io = SocketIO()

DeviceNameSpace = '/ws/device'
CloudPageNameSpace = '/ws/cloud/page'

from . import device_view, cloud_page_view
