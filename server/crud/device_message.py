import datetime

from sqlalchemy import select, func, text

from crud.base import CRUDBase
from models import Device
from models.device_message import DeviceMessage


class CRUDDeviceMessage(CRUDBase[DeviceMessage]):
    def count_detections(self):
        with self.DB() as db:
            subquery = (select([func.max(DeviceMessage.id)]).group_by(DeviceMessage.device_serial_no))
            query = (select(DeviceMessage.detect_times).where(DeviceMessage.id.in_(subquery)).group_by(
                DeviceMessage.device_serial_no))
            result = db.execute(query).all()
            detections_count = sum([_[0] for _ in result])
            return detections_count

    def count_changes(self, query_data):
        with self.DB() as db:
            subquery = select([func.max(DeviceMessage.id)])
            if query_data['start_time']:
                subquery = subquery.filter(self.model.created_at >= query_data['start_time'])
            if query_data['end_time']:
                subquery = subquery.filter(self.model.created_at <= query_data['end_time'])
            subquery = (subquery.group_by(DeviceMessage.device_serial_no))
            query = (select(DeviceMessage.power_change_times).where(DeviceMessage.id.in_(subquery)).group_by(
                DeviceMessage.device_serial_no))
            result = db.execute(query).all()
            detections_count = sum([_[0] for _ in result])
            return detections_count

    def count_risks(self, today=False):
        with self.DB() as db:
            if today:
                subquery = (select([func.max(DeviceMessage.id)]).where(
                    DeviceMessage.created_at >= datetime.datetime.combine(datetime.date.today(),
                                                                          datetime.time.min)).group_by(
                    DeviceMessage.device_serial_no))
            else:
                subquery = (select([func.max(DeviceMessage.id)]).group_by(DeviceMessage.device_serial_no))
            query = (select(DeviceMessage.risk_times).where(DeviceMessage.id.in_(subquery)).group_by(
                DeviceMessage.device_serial_no))
            result = db.execute(query).all()
            risks_count = sum([_[0] for _ in result])
            return risks_count

    def count_risk_target(self, risk_target):
        ...

    def get_station_status_device(self, station_name):
        with self.DB() as db:
            sql_result = db.query(self.model.created_at, self.model.device_temperature, self.model.device_cpu_usage,
                                  self.model.device_mem_usage,
                                  self.model.device_disk_usage) \
                .join(Device, self.model.device_serial_no == Device.device_serial_no).filter(
                Device.station_name == station_name).order_by(self.model.id.desc()).limit(10).all()
            result = {'times': [_[0] for _ in reversed(sql_result)],
                      'device_temperature': [_[1] for _ in reversed(sql_result)],
                      'device_cpu_usage': [_[2] for _ in reversed(sql_result)],
                      'device_mem_usage': [_[3] for _ in reversed(sql_result)],
                      'device_disk_usage': [_[4] for _ in reversed(sql_result)]}
            return result

    def get_station_status_camera(self, station_name):
        with self.DB() as db:
            sql_result = db.query(self.model.camera_connect_status, self.model.camera_temperature) \
                .join(Device, self.model.device_serial_no == Device.device_serial_no).filter(
                Device.station_name == station_name).order_by(self.model.id.desc()).first()
            if sql_result:
                result = {'camera_connect_status': sql_result[0], 'camera_temperature': sql_result[1]}
            else:
                result = {'camera_connect_status': True, 'camera_temperature': 0.0}
            return result

    def get_one_by_station_name(self, station_name) -> DeviceMessage:
        with self.DB() as db:
            return db.query(self.model).join(Device, self.model.device_serial_no == Device.device_serial_no).filter(
                Device.station_name == station_name).first()

    def get_data_within_one_day(self, device_serial_no):
        with self.DB() as db:
            return db.query(self.model).filter(self.model.device_serial_no == device_serial_no).filter(
                self.model.created_at > datetime.datetime.today().strftime('%Y-%m-%d') + ' 00:00:00').order_by(
                self.model.id.desc()).first()


crud_device_message = CRUDDeviceMessage(DeviceMessage)
