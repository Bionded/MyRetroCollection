import logging
import os

class logs_manager:
    def __init__(self,core):
        self.name = "logs_manager"
        self.__core = core
        self.config_manager = self.__core.config_manager
        self.plugin_manager = self.__core.plugin_manager
        self.logger_plugins = []
        self.logger = logger(self)

    def updatePluginManager(self):
        self.plugin_manager = self.__core.plugin_manager
        self.logger.plugin_manager = self.plugin_manager



    def getLogger(self):
        return self.logger


class logger:
    def __init__(self, _logger_manager):
        self.name = "logger"
        self.logger_manager = _logger_manager
        self.default_log_folder = "Logs"
        self.plugin_manager = self.logger_manager.plugin_manager
        self.logger_plugins = []
        self.fallback_logger = self._fallbackLogger()

    def updatePluginManager(self):
        self.logger_manager.updatePluginManager()
        self.plugin_manager = self.logger_manager.plugin_manager

    def _fallbackLogger(self):
        name = "fallback_logger"
        log_file = "fallback.log"
        log_dir = self.default_log_folder
        formatting = '%(asctime)s %(levelname)-8s %(message)s'
        date_format = '%a, %d %b %Y %H:%M:%S'
        level = "DEBUG"

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_format = logging.Formatter(fmt=formatting, datefmt=date_format)
        handler = logging.FileHandler(os.path.join(log_dir, log_file))
        handler.setFormatter(log_format)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def add_logger(self, logger):
        self.logger_manager.logger_plugins.append(logger)
        self.logger_plugins.append(logger)
        self.plugin_manager = self.logger_manager.plugin_manager
        

    def remove_logger(self, logger):
        self.logger_manager.logger_plugins.remove(logger)
        self.logger_plugins.remove(logger)


    def INFO(self, sender, msg):
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreAnyLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PreAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreInfoLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PreInfoLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnInfoLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnInfoLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostInfoLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostInfoLogger: {e}''')
        else:
            self.fallback_logger.info(msg)

    def CRITICAL(self, sender, msg):
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreAnyLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin}in function PreAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreCriticalLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PreCriticalLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnCriticalLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnCriticalLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostCriticalLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostCriticalLogger: {e}''')
        else:
            self.fallback_logger.critical(msg)

    def ERROR(self, sender, msg):
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreAnyLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin}in function PreAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreErrorLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PreErrorLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnErrorLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnErrorLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostErrorLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostErrorLogger: {e}''')
        else:
            self.fallback_logger.error(msg)

    def WARNING(self, sender, msg):
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreAnyLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin}in function PreAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreWarningLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PreWarningLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnWarningLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnWarningLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostWarningLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostWarningLogger: {e}''')
        else:
            self.fallback_logger.warning(msg)

    def DEBUG(self, sender, msg):
        if len(self.logger_plugins) > 0 and self.plugin_manager:
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreAnyLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin}in function PreAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    return_msg = self.logger_manager.plugin_manager.DoCommand(sender, 'PreDebugLogger', msg)
                    if return_msg:
                        msg = return_msg
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PreDebugLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'OnDebugLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function OnDebugLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostAnyLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostAnyLogger: {e}''')
            for plugin in self.logger_plugins:
                try:
                    self.logger_manager.plugin_manager.DoCommand(sender, 'PostDebugLogger', msg)
                except Exception as e:
                    self.fallback_logger.error(f'''Error in plugin {plugin} in function PostDebugLogger: {e}''')
        else:
            self.fallback_logger.debug(msg)


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


