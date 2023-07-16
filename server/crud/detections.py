import datetime
import pandas as pd

from sqlalchemy import text, func, distinct

from crud.base import CRUDBase
from crud.utils import statistics_data_fill
from models import Device
from models.detection import Detection


class CRUDDetection(CRUDBase[Detection]):
    def get_exceptions_count(self, query_data):
        with self.DB() as db:
            query = db.query(self.model)
            return self.query_time_range(query_data, query).filter(self.model.report_code != 0).count()

    def get_swap_statistics(self, query_data):
        with self.DB() as db:
            query = db.query(self.model.device_serial_no, Device.station_name, func.count())
            query = self.query_time_range(query_data, query)
            query = query.join(Device, self.model.device_serial_no == Device.device_serial_no)
            result = query.group_by(self.model.device_serial_no).all()
            result = statistics_data_fill(result)
            return result

    def get_exception_statistics(self, query_data):
        with self.DB() as db:
            query = db.query(self.model.device_serial_no, Device.station_name, func.count()).filter(
                self.model.report_code != 0)
            query = self.query_time_range(query_data, query)
            query = query.join(Device, self.model.device_serial_no == Device.device_serial_no)
            result = query.group_by(self.model.device_serial_no).all()
            result = statistics_data_fill(result)
            return result

    def get_station_detection_overview(self, query_data):
        with self.DB() as db:
            query = db.query(self.model)
            query = self.query_time_range(query_data, query)
            if query_data['device_serial_no']:
                query = query.filter(self.model.device_serial_no == query_data['device_serial_no'])
            elif query_data['station_name']:
                query = query.join(Device, self.model.device_serial_no == Device.device_serial_no).filter(
                    Device.station_name == query_data['station_name'])
            detect_success_times = query.filter(self.model.report_code == 0).count()
            detect_fail_times = query.filter(self.model.report_code != 0).count()
            return {'detect_success_times': detect_success_times, 'detect_fail_times': detect_fail_times}

    def get_station_detection_trend(self, query_data):
        result = {"dates": [], "power_change_total": [], "detect_success": [], "detect_fail": []}
        # if not query_data['time_range']:
        #     return result
        with self.DB() as db:
            extra_condition = ''
            device_serial_no = ''
            if query_data['device_serial_no']:
                device_serial_no = query_data['device_serial_no']
                extra_condition = " AND detection.device_serial_no = :device_serial_no"
            elif query_data['station_name']:
                device_serial_no_info = db.query(Device.device_serial_no).filter(
                    Device.station_name == query_data['station_name']).first()
                if device_serial_no_info and device_serial_no_info[0]:
                    # extra_condition = " AND detection.device_serial_no = '%s'" % device_serial_no_info[0]
                    device_serial_no = device_serial_no_info[0]
                    extra_condition = " AND detection.device_serial_no = :device_serial_no"
            count_conditions = {
                'detection_success': 'CASE WHEN (detection.report_code = 0&{extra_condition}) THEN 1 END'.replace(
                    '&{extra_condition}', extra_condition),
                'detection_fail': 'CASE WHEN (detection.report_code != 0&{extra_condition}) THEN 1 END'.replace(
                    '&{extra_condition}', extra_condition),
                'power_change_all': 'CASE WHEN (detection.plc_work_flow = 1&{extra_condition}) THEN 1 END'.replace(
                    '&{extra_condition}', extra_condition)}
            daily_counts = {}
            for count_condition_k, count_condition_v in count_conditions.items():
                query = db.query(func.date(self.model.created_at).label('day'),
                                 func.ifnull(func.count(
                                     text(count_condition_v)),
                                     0).label('count'))
                query = self.query_time_range(query_data, query)
                query = query.params(device_serial_no=device_serial_no) \
                    .group_by(func.date(self.model.created_at)) \
                    .order_by(func.date(self.model.created_at).asc())
                daily_counts[count_condition_k] = query.all()
            result = {"dates": [], "power_change_total": [], "detect_success": [], "detect_fail": []}
            for i in range(len(daily_counts['detection_success'])):
                result['dates'].append(daily_counts['detection_success'][i][0])
                result['detect_success'].append(daily_counts['detection_success'][i][1])
                result['power_change_total'].append(daily_counts['power_change_all'][i][1])
                result['detect_fail'].append(daily_counts['detection_fail'][i][1])
            # fill null data
            if query_data['time_range']:
                dates = get_all_date_from_range(query_data['start_time'], query_data['end_time'])
            else:
                dates = get_all_date_from_range(result['dates'][0], result['dates'][-1], '%Y-%m-%d', time_type='date')
            # fill_detection_trend(dates, result)
            return fill_detection_trend(dates, result)

    # todo
    def create_with_merge(self, obj_in):
        with self.DB() as db:
            if obj_in:
                device_serial_no = obj_in[0]['device_serial_no']
                detection_ids = db.query(distinct(self.model.detection_id)).filter(
                    self.model.device_serial_no == device_serial_no).all()
                objs = [self.model(**_) for _ in obj_in if _['detection_id'] not in detection_ids]
                db.bulk_save_objects(objs)
                db.commit()
                # self.DB.refresh()
                return objs

    def get_detections(self, query_data):
        query = self.query_time_range(query_data, order_desc=True)
        if query_data['station_name']:
            query = query.join(Device, self.model.device_serial_no == Device.device_serial_no).filter(
                Device.station_name == query_data['station_name'])
        if query_data['device_serial_no']:
            query = query.filter(self.model.device_serial_no == query_data['device_serial_no'])
        total = query.with_entities(func.count(self.model.id)).scalar()
        data = query.offset(query_data['offset']).limit(query_data['limit']).all()
        return {'rows': data, 'total': total}


crud_detection = CRUDDetection(Detection)


def get_all_date_from_range(start_time, end_time, time_format='%Y-%m-%d %H:%M:%S', time_type='str'):
    if time_type == 'str':
        start_time = datetime.datetime.strptime(start_time, time_format)
        end_time = datetime.datetime.strptime(end_time, time_format)
    delta_days = (end_time - start_time).days
    # delta_days = (end_datetime - start_datetime).days
    dates = []
    for i in range(delta_days + 1):
        _date = start_time + datetime.timedelta(days=i)
        _date_str = _date.strftime('%Y-%m-%d')
        dates.append(_date_str)
    return dates


def fill_detection_trend(dates, trend_data):
    # print(dates, trend_data)
    # date_length = len(dates)
    df_index = ['detect_success', 'power_change_total', 'detect_fail']
    df = pd.DataFrame(0, columns=dates, index=df_index)

    for i in range(len(trend_data['dates'])):
        for di in df_index:
            trend_data_date = trend_data['dates'][i].strftime('%Y-%m-%d')
            df[trend_data_date][di] = trend_data[di][i]
    result = {'dates': dates,
              'detect_success': df.loc['detect_success'].to_list(),
              'power_change_total': df.loc['power_change_total'].to_list(),
              'detect_fail': df.loc['detect_fail'].to_list()}
    return result
