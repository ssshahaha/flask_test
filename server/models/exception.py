from sqlalchemy import Column, String, Boolean, Integer, Float

from db.base_class import Base


# Fixed data for mapping
class DeviceException(Base):
    exception_code = Column(String(10))
    stage = Column(String(64))
    type = Column(String(64))
    prompt = Column(String(255))
    reason = Column(String(64))
    solution = Column(String(255))
    report_code = Column(Integer)
    plc_work_flow = Column(Integer)
