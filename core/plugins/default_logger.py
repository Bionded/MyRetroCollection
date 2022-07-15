import os
import logging
class default_logger():
    def __init__(self, plugin_manager):
        self.name = "Default Logger"
        self.version = "0.0.1"
        self.author = "Bionded"
        self.description = "Default logger plugin"
        self.website = ""
        self.license = "GPLv3"
        self.config_file = "logger.conf"
        self.config_section = "DefaultLogger"
        self.dependencies = ['logging']
        self.plugin_manager = plugin_manager
        self.store_logger = self.plugin_manager.logger
        self.logger = self.store_logger
        self.configs = self.plugin_manager.config_manager.getConfig(self)

    def disable(self):
        self.store_logger.remove_logger(type(self).__name__)

    def enable(self):
        self.store_logger.add_logger(type(self).__name__)
        self.store_logger.updatePluginManager()
        self.logger = self._initLogger()

    def _initLogger(self):
        log_file = self.configs.getValue('log_file', 'retro_collection.log')
        if not log_file.startswith('/'):
            if '/' in log_file:
                log_dir = os.path.dirname(log_file)
                log_file = log_file.split('/')[-1]
            else:
                log_dir = self.store_logger.default_log_folder
        else:
            log_dir = os.path.dirname(log_file)
        formatting = self.configs.getValue("log_format", '%(levelname)-8s %(message)s')
        date_format = self.configs.getValue("log_date_format", '%Y-%m-%d %H:%M:%S')
        level = self.configs.getValue("log_level", "INFO")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_format = logging.Formatter(fmt=formatting, datefmt=date_format)
        handler = logging.FileHandler(os.path.join(log_dir, log_file))
        handler.setFormatter(log_format)
        logger = logging.getLogger(self.name + '_' + self.version)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def PreAnyLogger(self, sender, message):
        return f"{sender.name}: {message}"

    def OnInfoLogger(self, sender, message):
        self.logger.info(message)

    def OnWarningLogger(self, sender, message):
        self.logger.warning(message)

    def OnErrorLogger(self, sender, message):
        self.logger.error(message)

    def OnDebugLogger(self, sender, message):
        self.logger.debug(message)

    def OnCriticalLogger(self, sender, message):
        self.logger.critical(message)

