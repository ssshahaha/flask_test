import datetime
import jwt
import hashlib

from config import AppConfig
from commons.json_cls import JsonEncoder


class Authentication:
    def __init__(self):
        self.token_salt = AppConfig.TokenSalt
        self.token_minutes = AppConfig.LoginDurationMinutes

    def encode(self, user_info, token_minutes=None):
        token_minutes = token_minutes or self.token_minutes
        ttl = datetime.timedelta(minutes=token_minutes)
        payload = {
            'exp': datetime.datetime.utcnow() + ttl,
            'iat': datetime.datetime.utcnow(),
            'iss': 'aicv_cloud',
            'data': user_info,
        }
        _string = jwt.encode(
            payload=payload,
            key=self.token_salt,
            algorithm='HS256',
            json_encoder=JsonEncoder,
        )
        if isinstance(_string, bytes):
            _string = _string.decode('utf-8')
        return _string

    def decode(self, encode_str, token_minutes=None):
        """如果decode失败，将抛出异常"""
        token_minutes = token_minutes or self.token_minutes
        ttl = datetime.timedelta(minutes=token_minutes)
        payload = jwt.decode(
            jwt=encode_str,
            key=self.token_salt,
            algorithms='HS256',
            leeway=ttl,
        )
        return payload

    def md5_encrypt(self, input_str: str):
        md5 = hashlib.md5(self.token_salt.encode("utf8"))
        md5.update(input_str.encode("utf8"))
        result = md5.hexdigest()
        return result


Auth = Authentication()
