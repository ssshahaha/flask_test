import os
import sys

from loguru import logger


# class LogFilter(logging.Filter):
#     def filter(self, record: logging.LogRecord) -> bool:
#         if "/page/logs" in record.getMessage():
#             return False
#         return True


def init_logger(log_config=None):
    if log_config is None:
        log_config = {}
    # remove default log handler
    logger.remove()

    for log_name in log_config.get('LogNames', [{'name': 'app', 'to_console': True}]):
        _add_logger(log_name['name'], log_config, to_console=log_name['to_console'])

    # # filter logs from /page/logs route
    # log = logging.getLogger('werkzeug')
    # log.addFilter(LogFilter())


def _add_logger(name: str, log_config, *, to_console: bool = True):
    log_level = log_config.get("LOG_LEVEL", 10)
    log_keep_days = str(log_config.get("LOG_KEEP_DAY", 90)) + " days"
    # logger.bind(name='location').debug(f"log level: {log_level}, log keep days: {log_keep_days}")

    if to_console is True:
        logger.add(sys.stderr, filter=lambda record: record['extra']['name'] == name, )

    logger.add(
        os.path.join(log_config.get("LOG_DIR", ''), f"{name}.log"),
        level=log_level,
        retention=log_keep_days,
        backtrace=True,
        diagnose=log_config.get("DEBUG", False),
        rotation="00:00",
        compression="zip",
        filter=lambda record: record["extra"]["name"] == name,
        encoding='utf8',
        enqueue=True
    )


__all__ = [init_logger]

if __name__ == '__main__':
    init_logger()
    logger = logger.bind(name='app')
    logger.info('test')
    logger.debug('test')
    logger.error('test')
    logger.warning('test')
