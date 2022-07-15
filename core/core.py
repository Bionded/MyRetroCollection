import os
from .managers.pluginManager import plugin_manager
from .managers.logsManager import logs_manager
from .managers.configManager import config_manager
#from parts.collector import Collector


class core:
    def __init__(self):
        self.name = "core"
        self.config_section = "Core"
        self.version = "0.0.1"
        self.plugin_manager = None
        self.config_manager = None
        self.logs_manager = None
        self.logs_manager = logs_manager(self)
        self.config_manager = config_manager(self)
        self.logger = self.logs_manager.getLogger()
        self.config = self.config_manager.getConfig(self)
        self.plugin_manager = plugin_manager(self)
        self.plugin_manager.enable()

    def test(self):
        self.logger.info(self, "test info")
        self.logger.debug(self, "test debug")
        self.logger.error(self, "test error")
        print(self.plugin_manager.getAllPluginsInfo())
        self.plugin_manager.enablePlugin('default_logger')
        test = self.plugin_manager.DoCommand('core', 'OnTest','testing from core')
        print(test)