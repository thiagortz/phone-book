import logging
from logging import Logger

FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
DATE_FMT = '%m-%d %H:%M:%S'

LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL,
                    format=FORMAT,
                    datefmt=DATE_FMT)


class LoggerManager(Logger):
    def __init__(self, name):
        self._logger = logging.getLogger(name)

    def logger(self):
        return self._logger

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._logger.warn(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self._logger.log(msg, *args, **kwargs)
