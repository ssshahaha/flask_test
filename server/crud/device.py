import datetime

from sqlalchemy import func, distinct

from commons.func_tools import get_random_str
from crud.base import CRUDBase
from models.device import Device


class CRUDDevice(CRUDBase[Device]):
    def get_by_serial_no(self, serial_no):
        with self.DB() as db:
            return db.query(Device).filter(Device.device_serial_no == serial_no, Device.is_delete == False).first()

    def get_one_by_field(self, field_name, field_value):
        with self.DB() as db:
            return db.query(Device).filter(getattr(Device, field_name) == field_value,
                                           Device.is_delete == False).first()

    def search_one(self, search_data: dict):
        with self.DB() as db:
            query = db.query(Device).filter(Device.is_delete == False)
            for search_k, search_v in search_data.items():
                if search_v:
                    query = query.filter(getattr(Device, search_k) == search_v)
            return query.first()

    def device_register(self, device_data):
        device = self.get_by_serial_no(device_data.get('device_serial_no', ''))
        if not device:
            # 防止station_name重名
            if not device_data['station_name']:
                device_data['station_name'] = '换电站_' + get_random_str(6)
            else:
                if self.get_one_by_field('station_name', device_data['station_name']):
                    device_data['station_name'] = device_data['station_name'] + get_random_str(6)
            device = self.create(device_data)
        else:
            device = self.update(device, device_data)
        self.update(device, {'online_status': True})

    def get_devices(self, query_data):
        with self.DB() as db:
            query = db.query(Device).filter(Device.is_delete == False)
            if query_data['online_status'] != 'all':
                online_status = True if query_data['online_status'] == 'true' else False
                query = query.filter(Device.online_status == online_status)
            total = query.with_entities(func.count(Device.id)).scalar()
            devices = query.offset(query_data['offset']).limit(query_data['limit']).all()
            return {'total': total, 'devices': devices}

    def get_online_stations(self):
        with self.DB() as db:
            items = db.query(distinct(Device.station_name)).filter(Device.is_delete == False,
                                                                   Device.online_status == True).all()
            items = [_[0] for _ in items if _[0]]
            total = len(items)
            return {'total': total, 'items': items}

    def count_devices(self):
        with self.DB() as db:
            total = db.query(Device).filter(Device.is_delete == False).count()
            online_total = db.query(Device).filter(Device.is_delete == False, Device.online_status == True).count()
            return {'total': total, 'online_total': online_total}

    def get_devices_field_list(self, device_field):
        with self.DB() as db:
            field_values = db.query(distinct(getattr(Device, device_field))).filter(Device.is_delete == False).all()
            return [_[0] for _ in field_values if _[0]]

    def count_risk_target(self, risk_target):
        with self.DB() as db:
            return db.query(self.model).filter(
                getattr(self.model, risk_target + '_risk_status', Device.is_delete == False) == True).count()

    def get_stations_names(self):
        with self.DB() as db:
            items = db.query(Device.device_serial_no, Device.station_name).filter(Device.is_delete == False,
                                                                                  Device.online_status == True).all()
            # items = [{'device_serial_no': _[0], 'station_name': _[1]} for _ in items]
            # items = [{_[0]: _[1]} for _ in items]
            station_names = [_[1] for _ in items]
            device_serial_nos = [_[0] for _ in items]
            total = len(items)
            result = dict()
            result['online'] = {'total': total, 'station_names': station_names, 'device_serial_nos': device_serial_nos}
            items = db.query(Device.device_serial_no, Device.station_name).filter(Device.is_delete == False,
                                                                                  Device.online_status == False).all()
            station_names = [_[1] for _ in items]
            device_serial_nos = [_[0] for _ in items]
            total = len(items)
            result['offline'] = {'total': total, 'station_names': station_names, 'device_serial_nos': device_serial_nos}
            return result

    def update_by_device_serial_no(self, device_serial_no):
        self.update_by_field('device_serial_no', device_serial_no, {'updated_at': datetime.datetime.now()})

    def get_all_name_no(self):
        with self.DB() as db:
            return db.query(self.model.device_serial_no, self.model.station_name).filter(
                Device.is_delete == False).all()


crud_device = CRUDDevice(Device)
