from sqlalchemy import Column, String, Boolean, Text, Float

from db.base_class import Base


class Device(Base):
    device_name = Column(String(64), default='', nullable=False)
    device_address = Column(String(255), default='', nullable=False)
    station_name = Column(String(64), default='', nullable=False)
    device_serial_no = Column(String(64), default='', nullable=False)
    device_customer = Column(String(20), default='', nullable=False)
    app_version = Column(String(64), default='', nullable=False)
    model_version = Column(String(255), default='', nullable=False)
    is_delete = Column(Boolean(), default=False, nullable=False)
    online_status = Column(Boolean(), default=False, nullable=False)
    device_config = Column(Text, default='{}', nullable=False)
    device_risk_status = Column(Boolean(), default=False, nullable=False)
    camera_risk_status = Column(Boolean(), default=False, nullable=False)
    # coordinate_x = Column(Float, default=0.0)
    # coordinate_y = Column(Float, default=0.0)
