from sqlalchemy import text, func

from commons.func_tools import dict_field_values
from crud.base import CRUDBase
from crud.utils import statistics_data_fill
from models import Device
from models.risk import Risk


class CRUDRisk(CRUDBase[Risk]):
    def get_risks_overview(self):
        with self.DB() as db:
            query_fields = ['device_serial_no', 'limit_value', 'target', 'category', 'id', 'created_at', 'value',
                            'is_handled', 'updated_at']
            query = text(f'''select {','.join(query_fields)} from(
            select *,IF(@group_field=device_serial_no,@group_size:=@group_size+1,@group_size:=0) 'group_size',
            @group_field:=device_serial_no 'group_field' from risk order by id desc)
            a where a.group_size<5''')
            result = db.execute(query).all()
            return dict_field_values(query_fields, result)

    def get_risks(self, query_data):
        with self.DB() as db:
            query = db.query(self.model)
            if query_data['search'] != 'all':
                query = query.filter(self.model.is_handled == query_data['is_handled'])
                if query_data['risk_target']:
                    query = query.filter(self.model.target == query_data['risk_target'])
                if query_data['station_name']:
                    query = query.filter(Device.station_name == query_data['station_name']).join(Device,
                                                                                                 Device.device_serial_no == self.model.device_serial_no)
                if query_data['message']:
                    query = query.filter(self.model.message.like(f'%{query_data["message"]}%'))
            total = query.with_entities(func.count(self.model.id)).scalar()
            items = query.offset(query_data['offset']).limit(query_data['limit']).all()
            return {'total': total, 'rows': items}

    def get_risk_statistics(self, query_data) -> dict:
        with self.DB() as db:
            query = db.query(self.model.device_serial_no, Device.station_name, func.count()).filter(
                self.model.is_handled == False)
            query = self.query_time_range(query_data, query)
            query = query.join(Device, self.model.device_serial_no == Device.device_serial_no)
            result = query.group_by(self.model.device_serial_no).all()
            result = statistics_data_fill(result)
            return result


crud_risk = CRUDRisk(Risk)
