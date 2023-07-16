from sqlalchemy import Column, String, Boolean, Integer, Float

from db.base_class import Base


class Detection(Base):
    device_serial_no = Column(String(64), default='', nullable=False)
    # detection_id = Column(String(64), nullable=False, unique=True)
    detection_id = Column(String(64), nullable=False)
    detection_create_time = Column(String(64), nullable=False, default='')
    detection_update_time = Column(String(64), nullable=False, default='')
    report_code = Column(Integer, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)
    angle = Column(Float, nullable=False)
    depths = Column(String(64), nullable=False, default='')
    spent_ms = Column(Integer, nullable=False)
    image_path = Column(String(255), nullable=False, default='')
    # result = Column(String(64), nullable=False, default='')
    request_address = Column(Integer, nullable=False)
    plc_work_flow = Column(Integer, nullable=False)
    detection_type = Column(String(64), nullable=False, default='')  # plc,api
