import os
from .parts.collector import Collector
from .managers.pluginManager import plugin_manager
from .managers.logsManager import logs_manager
from .managers.configManager import config_manager
#from parts.collector import Collector


class core:
    def __init__(self):
        self.plugin_manager = None
        self.config_manager = None
        self.logs_manager = None
        self.collector = None
        self.conf_path = "config/backend.conf"
        self.logs_manager = logs_manager(self)
        self.logger = self.logs_manager.getLogger()
        self.plugin_manager = plugin_manager(self)
        #self.config_manager = config_manager(self)
        #self.plugin_manager = plugin_manager(self)

    def test(self):
        print(self.plugin_manager.getAllPluginsInfo())
        print("test")