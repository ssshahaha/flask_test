from sqlalchemy import Boolean, Column, Integer, String, Float, Text

from db.base_class import Base


class DeviceMessage(Base):
    device_serial_no = Column(String(64), default='', nullable=False)
    last_calibrate_time = Column(String(20), default='', nullable=False)
    app_version = Column(String(64), default='', nullable=False)
    model_version = Column(String(255), default='', nullable=False)
    plc_connect_status = Column(Boolean(), default=True)
    camera_connect_status = Column(Boolean(), default=True)
    station_connect_status = Column(Boolean(), default=True)
    device_temperature = Column(Float, default=0.0)
    device_cpu_usage = Column(Float, default=0.0)
    device_mem_usage = Column(Float, default=0.0)
    device_disk_usage = Column(Float, default=0.0)
    camera_temperature = Column(Float, default=0.0)
    power_change_times = Column(Integer, default=0, nullable=False)
    detect_times = Column(Integer, default=0, nullable=False)
    detect_success_times = Column(Integer, default=0, nullable=False)
    detect_success_rate = Column(Float, default=0.0, nullable=False)
    detect_fail_times = Column(Integer, default=0, nullable=False)
    detect_fail_rate = Column(Float, default=0.0, nullable=False)
    risk_times = Column(Integer, default=0, nullable=False)
    exception_times = Column(Integer, default=0, nullable=False)
    daily_detect_times = Column(Integer, default=0, nullable=False)
    week_statistics_data = Column(Text, default='')
