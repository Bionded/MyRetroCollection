import logging
import os

class logs_manager:
    def __init__(self,core):
        self.name = "logs_manager"
        self.__core = core
        self.config_manager = self.__core.config_manager
        self.primary_logger = None  # Todo: change to primary_logger to plugin_manager.get_plugin("main_logger")
        self.logger = logger(self)

    def changePrimaryLogger(self):
        self.logger.updatePrimaryLogger()

    def getLogger(self):
        return self.logger


class logger:
    def __init__(self, _logger_manager):
        self.name = "fallback_logger"
        self.logger_manager = _logger_manager
        self.log_file = "Logs/fallback.log"
        self.log_dir = os.path.dirname(self.log_file)
        self.formatting = '%(asctime)s %(levelname)-8s %(message)s'
        self.date_format = '%a, %d %b %Y %H:%M:%S'
        self.level = "INFO"
        if self.logger_manager.primary_logger:
            self.updatePrimaryLogger()
        else:
            self.primary_logger = self.logger_manager.primary_logger
        self.fallback_logger = self._fallbackLogger()

    def updatePrimaryLogger(self):
        if self.logger_manager.config_manager:
            pass
        self.fallback_logger = self._fallbackLogger()


    def _fallbackLogger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_format = logging.Formatter(fmt=self.formatting, datefmt=self.date_format)
        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(log_format)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(handler)
        return logger

    def INFO(self, msg):
        self.fallback_logger.info(msg)

    def DEBUG(self, msg):
        self.fallback_logger.debug(msg)

    def WARNING(self, msg):
        self.fallback_logger.warning(msg)

    def ERROR(self, msg):
        self.fallback_logger.error(msg)

    def CRITICAL(self, msg):
        self.fallback_logger.critical(msg)

    def info(self, msg):
        self.fallback_logger.info(msg)

    def debug(self, msg):
        self.fallback_logger.debug(msg)

    def warning(self, msg):
        self.fallback_logger.warning(msg)

    def error(self, msg):
        self.fallback_logger.error(msg)

    def critical(self, msg):
        self.fallback_logger.critical(msg)

