import logging
import os

class logs_manager:
    def __init__(self, core):
        self.name = "logs_manager"
        self.version = "0.0.1"
        self._core = core
        self.config_manager = self._core.config_manager
        self.plugin_manager = self._core.plugin_manager
        self.config = self.config_manager.getConfig(self)
        self.loggers ={}
        self.loggers['default'] = logger(self)

    def __repr__(self):
        return f"{self.name} v{self.version}"

    def updatePlugins(self):
        self.plugin_manager = self._core.plugin_manager
        for logger in self.loggers.values():
            logger.updatePlugins()
    def getLogger(self,called_by=None):
        if called_by is None:
            return self.loggers['default']
        elif 'different_log' in dir(called_by) and called_by.different_log is False:
            return self.loggers['default']
        elif called_by.name in self.loggers:
            return self.loggers[called_by.name]
        else:
            self.loggers[called_by.name] = logger(self, called_by)

        return self.loggers[called_by.name]


class logger:
    def __init__(self, _logger_manager, called_by=None):
        self.caller = called_by
        self.name = 'logger'
        if 'config' in dir(self.caller):
            self.call_config = self.caller.config
        else:
            self.call_config = None
        self.logger_manager = _logger_manager
        self.version = self.logger_manager.version
        self.default_log_folder = "Logs"
        self.plugin_manager = self.logger_manager.plugin_manager
        self.config = self.logger_manager.config_manager.getConfig(self)
        self.allowed_plugins_types = ['logger']
        self.logger_plugins = []
        self.logger = self.init_logger()

    def __repr__(self):
        return f"{self.name} v{self.version}"

    def updatePlugins(self):
        self.plugin_manager = self.logger_manager.plugin_manager
        temp = []
        for plugin in self.plugin_manager.enabled_plugins.values():
            if plugin.type in self.allowed_plugins_types:
                temp.append(plugin.name)
        self.logger_plugins = temp

    def init_logger(self):
        if self.call_config and self.call_config.getBool('different_log', False) is False:
            self.call_config = self.config
            self.caller = None
        elif self.call_config is None:
            self.call_config = self.config
            self.caller = None
        log_file = self.call_config.getValue('log_file', self.config.getValue('log_file', 'retro_collection.log'))
        log_dir = self.call_config.getValue('log_dir', self.config.getValue('log_dir', self.default_log_folder))
        if not log_file.startswith('/'):
            if '/' in log_file:
                log_file = log_file.split('/')[-1]
        else:
            log_dir = os.path.dirname(log_file)
        formatting = self.call_config.getValue('log_format', self.config.getValue('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        date_format = self.call_config.getValue('log_date_format', self.config.getValue("log_date_format", '%Y-%m-%d %H:%M:%S'))
        level = self.call_config.getValue('log_level', self.config.getValue("log_level", "INFO"))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_format = logging.Formatter(fmt=formatting, datefmt=date_format)
        handler = logging.FileHandler(os.path.join(log_dir, log_file))
        handler.setFormatter(log_format)
        if self.caller:
            self.name = self.caller.name
        logger = logging.getLogger(self.name + '_' + self.logger_manager.version)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def INFO(self, sender, msg):
        self.logger.info(f"[{sender}] {msg}")
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                if sender.name == plugin:
                    continue
                try:
                    self.plugin_manager.doCommand(sender, 'InfoLogger', plugin, msg)
                except Exception as e:
                    self.logger.error(f'''Error in plugin {plugin} in function InfoLogger: {e}''')

    def DEBUG(self, sender, msg):
        self.logger.debug(f"[{sender}] {msg}")
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                if sender.name == plugin:
                    continue
                try:
                    self.plugin_manager.doCommand(sender, 'DebugLogger', plugin, msg)
                except Exception as e:
                    self.logger.error(f'''Error in plugin {plugin} in function DebugLogger: {e}''')

    def WARNING(self, sender, msg):
        self.logger.warning(f"[{sender}] {msg}")
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                if sender.name == plugin:
                    continue
                try:
                    self.plugin_manager.doCommand(sender, 'WarningLogger', plugin, msg)
                except Exception as e:
                    self.logger.error(f'''Error in plugin {plugin} in function WarningLogger: {e}''')

    def ERROR(self, sender, msg):
        self.logger.error(f"[{sender}] {msg}")
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                if sender.name == plugin:
                    continue
                try:
                    self.plugin_manager.doCommand(sender, 'ErrorLogger', plugin, msg)
                except Exception as e:
                    self.logger.error(f'''Error in plugin {plugin} in function ErrorLogger: {e}''')

    def CRITICAL(self, sender, msg):
        self.logger.critical(f"[{sender}] {msg}")
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                if sender.name == plugin:
                    continue
                try:
                    self.plugin_manager.doCommand(sender, 'CriticalLogger', plugin, msg)
                except Exception as e:
                    self.logger.error(f'''Error in plugin {plugin} in function CriticalLogger: {e}''')




    def info(self, sender, msg):
        self.INFO(sender, msg)

    def debug(self, sender, msg):
        self.DEBUG(sender, msg)

    def warning(self, sender, msg):
        self.WARNING(sender, msg)

    def error(self, sender, msg):
        self.ERROR(sender, msg)

    def critical(self, sender, msg):
        self.CRITICAL(sender, msg)


