import redis

from config import AppConfig

REDIS = redis.StrictRedis.from_url(AppConfig.DB_RedisUri, decode_responses=True)


class RedisClient:
    def __init__(self):
        self.client = redis.StrictRedis.from_url(AppConfig.DB_RedisUri, decode_responses=True)

    def save_captcha(self, captcha_id: str, captcha_text: str):
        self.client.setex('login_captcha:' + captcha_id, AppConfig.CaptchaValidPeriodSeconds, captcha_text)

    def check_captcha(self, captcha_id: str, captcha_text: str):
        save_captcha_text = self.client.get('login_captcha:' + captcha_id)
        if save_captcha_text and save_captcha_text == captcha_text:
            return True
        else:
            return False

    def update_online_status(self, ws_id: str, device_serial_no: str, online_status: bool):
        if online_status:
            # self.client.set('online_status:' + ws_id, device_serial_no)
            self.client.setex('online_status:' + ws_id, 3600 * 24, device_serial_no)
            self.client.hset('register_device_sid', device_serial_no, ws_id)
        else:
            self.client.delete('online_status:' + ws_id)
            self.client.hdel('register_device_sid', device_serial_no)

    def check_device_sid(self, device_serial_no, sid):
        return sid == self.client.hget('register_device_sid', device_serial_no)

    def get_device_serial_no_by_ws_id(self, ws_id: str) -> str:
        return self.client.get('online_status:' + ws_id)

    def get_last_upload_detection_time(self, device_serial_no) -> str:
        return self.client.hget('lastUploadDetectionTime', device_serial_no) or ''

    def update_last_upload_detection_time(self, device_serial_no, upload_time: str):
        return self.client.hset('lastUploadDetectionTime', device_serial_no, upload_time)


redis_client = RedisClient()
