from flask import Blueprint

page = Blueprint('page', __name__, url_prefix='/page')

from . import view

page.add_url_rule("/login", view_func=view.page_login, methods=["POST"])  # 登录
page.add_url_rule("/register", view_func=view.page_register, methods=["POST"])  # 注册
page.add_url_rule("/captcha", view_func=view.page_captcha, methods=["GET"])  # 获取验证码
page.add_url_rule("/version", view_func=view.page_version, methods=["GET"])  # 获取版本号

page.add_url_rule("/devices", view_func=view.page_devices, methods=["GET"])  # 获取设备列表
page.add_url_rule("/devices/count", view_func=view.page_devices_count, methods=["GET"])  # 获取设备总数
page.add_url_rule("/devices/info", view_func=view.page_devices_info, methods=["GET"])  # 获取单个设备信息
page.add_url_rule("/devices/query/<device_field>", view_func=view.page_devices_query, methods=["GET"])  # 获取设备某属性所有值
page.add_url_rule("/devices/days", view_func=view.page_devices_days, methods=["GET"])  # 获取设备某属性所有值


page.add_url_rule("/detections", view_func=view.page_detections, methods=["GET"])  # 获取检测总数
page.add_url_rule("/detections/count", view_func=view.page_detections_count, methods=["GET"])  # 获取检测总数
page.add_url_rule("/swap/count", view_func=view.page_changes_count, methods=["GET"])  # 获取检测总数

page.add_url_rule("/risks", view_func=view.page_risks, methods=["GET"])  # 获取预警列表信息
page.add_url_rule("/risks/count", view_func=view.page_risks_count, methods=["GET"])  # 获取预警总数
# page.add_url_rule("/risks/count/today", view_func=view.page_risks_count_today, methods=["GET"])  # 获取今日预警总数
page.add_url_rule("/risks/count/<risk_target>", view_func=view.page_risk_target_count, methods=["GET"])  # 获取异常设备数
page.add_url_rule("/risks/overview", view_func=view.page_risks_overview, methods=["GET"])  # 获取预警概览，每个站5条预警数据
page.add_url_rule("/risks/query/<field>", view_func=view.page_risks_query_field, methods=["GET"])  # 获取预警某属性所有数据

page.add_url_rule("/exceptions", view_func=view.page_exceptions, methods=["GET"])  # 获取异常列表
page.add_url_rule("/exceptions/query/code", view_func=view.page_exceptions_query_code, methods=["GET"])  # 获取所有异常代码
page.add_url_rule("/exceptions/count", view_func=view.page_exceptions_count, methods=["GET"])  # 获取所有异常次数
page.add_url_rule("/exceptions/count/today", view_func=view.page_exceptions_count_today, methods=["GET"])  # 获取今日异常次数
# page.add_url_rule("/statistics/rank", view_func=view.page_statistics_rank, methods=["GET"])  # 获取换电统计
page.add_url_rule("/statistics/rank/<target>", view_func=view.page_statistics_rank_target, methods=["GET"])  # 获取换电统计

page.add_url_rule("/stations/online", view_func=view.page_stations_online, methods=["GET"])  # 获取在线换电站名称
page.add_url_rule("/stations/names", view_func=view.page_stations_names, methods=["GET"])  # 获取换电站名称
page.add_url_rule("/stations/status/device", view_func=view.page_stations_status_device, methods=["GET"])  # 获取站主机状态信息
page.add_url_rule("/stations/status/camera", view_func=view.page_stations_status_camera, methods=["GET"])  # 获取站相机状态信息
page.add_url_rule("/stations/status/camera/photo", view_func=view.page_stations_status_camera_photo,
                  methods=["POST"])  # 获取站相机拍照信息
page.add_url_rule("/stations/detection/overview", view_func=view.page_stations_detection_overview,
                  methods=["GET"])  # 获取站检测数据概览
page.add_url_rule("/stations/detection/trend", view_func=view.page_stations_detection_trend, methods=["GET"])  # 获取站检测趋势
page.add_url_rule("/stations/coordinate", view_func=view.page_stations_info, methods=["GET"])  # 获取单个站信息等 ...
page.add_url_rule("/stations/info", view_func=view.page_stations_info, methods=["GET"])  # 获取单个站信息等

page.add_url_rule("/image/<image_name>", view_func=view.page_image, methods=["GET"])  # 获取图片

page.add_url_rule("/upload/last/detection", view_func=view.page_upload_last_detection, methods=["GET"])  # 获取或更新最新检测上传时间
