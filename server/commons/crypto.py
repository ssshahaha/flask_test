import base64

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AesCryptoClient:
    IV = 'iv:cloud_server$'
    KEY = 'key:cloud_server'
    BLOCK_SIZE = 16

    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, data: str):
        data = self.pad(data)
        cipher = AES.new(self.KEY.encode('utf8'), AES.MODE_CBC, self.IV.encode('utf8'))
        encrypted_bytes = cipher.encrypt(data.encode('utf8'))
        encode_str = base64.b64encode(encrypted_bytes)
        enc_text = encode_str.decode('utf8')
        return enc_text

    def decrypt(self, data):
        data = data.encode('utf8')
        encode_bytes = base64.decodebytes(data)
        cipher = AES.new(self.KEY.encode('utf8'), AES.MODE_CBC, self.IV.encode('utf8'))
        text_decrypted = cipher.decrypt(encode_bytes)
        text_decrypted = self.unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted


class B64Crypto:
    @staticmethod
    def encrypt(data: str) -> str:
        data_bytes = data.encode('utf8')
        base64_bytes = base64.b64encode(data_bytes)
        base64_data = base64_bytes.decode('utf8')
        return base64_data

    @staticmethod
    def decrypt(data: str) -> str:
        base64_bytes = data.encode('utf8')
        data_bytes = base64.b64decode(base64_bytes)
        result = data_bytes.decode('utf8')


AesCrypto = AesCryptoClient()
