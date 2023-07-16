from sqlalchemy import Column, String, Boolean, Integer, Float

from db.base_class import Base


class Risk(Base):
    device_serial_no = Column(String(64), default='', nullable=False)
    target = Column(Integer)
    category = Column(Integer)
    value = Column(Float, default=0.0, nullable=False)
    limit_value = Column(Float, default=0.0, nullable=False)
    is_handled = Column(Boolean(), default=False, nullable=False)
    risk_id = Column(String(64), default='', nullable=False)
    message = Column(String(255), default='')
