from crud.base import CRUDBase
from models import Detection
from models.exception import DeviceException


class CRUDException(CRUDBase):
    def get_exceptions(self, query_data):
        with self.DB() as db:
            query = db.query(Detection, DeviceException).join(DeviceException,
                                                              (Detection.report_code == DeviceException.report_code) &
                                                              Detection.plc_work_flow == DeviceException.plc_work_flow)
            total = query.count()
            db_data = query.offset(query_data['offset']).limit(query_data['limit']).all()
            device_exception_data = [_[1] for _ in db_data]
            return {'total': total, 'exception_info': device_exception_data}


crud_exception = CRUDException(DeviceException)
