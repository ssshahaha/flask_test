import base64
import io

import cv2
import numpy as np
from PIL import Image


def np2b64(img_numpy, b64_fmt=True, img_format='jpeg'):
    img_io = io.BytesIO()
    img_pil = Image.fromarray(img_numpy[..., ::-1])
    img_pil.save(img_io, img_format.upper())
    if b64_fmt:
        img_b64 = f'data:image/{img_format};base64,' + base64.b64encode(img_io.getvalue()).decode()
    else:
        img_b64 = base64.b64encode(img_io.getvalue()).decode()
    return img_b64


def b642np(img_b64: str, str_split=True):
    if str_split:
        img_buff = np.frombuffer(base64.b64decode(img_b64.split('base64,')[-1]), dtype=np.uint8)
    else:
        img_buff = np.frombuffer(base64.b64decode(img_b64), dtype=np.uint8)
    img_data = cv2.imdecode(img_buff, 1)
    return img_data
