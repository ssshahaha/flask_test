import base64
from io import BytesIO

from captcha.image import ImageCaptcha

from config import AppConfig


def generate_captcha(captcha_text):
    image = ImageCaptcha(width=AppConfig.CaptchaWidth, height=AppConfig.CaptchaHeight).generate_image(captcha_text)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    data = buffer.getvalue()
    return 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
