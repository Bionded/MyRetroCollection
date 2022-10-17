import os
from .managers.pluginManager import plugin_manager
from .managers.logsManager import logs_manager
from .managers.configManager import config_manager
from .managers.fsManager import fs_manager
from .managers.dbManager import db_manager
#from parts.collector import Collector
from .utils.types import *

class core:
    def __init__(self):
        self.name = "Core"
        self.config_section = "Core"
        self.version = "0.0.1"
        self.folder = os.path.dirname(os.path.abspath(__file__))
        self.plugin_manager = None
        self.config_manager = None
        self.logs_manager = None
        self.different_log = False
        self.log_file = None
        self.config_manager = config_manager(self)
        self.logs_manager = logs_manager(self)
        self.config = self.config_manager.getConfig(self)
        self.logger = self.logs_manager.getLogger(self)
        self.plugin_manager = plugin_manager(self)
        self.plugin_manager.enable()

        #self.fs_manager = fs_manager(self)
        #self.fs = self.fs_manager.get_fs_driver()
        self.db_manager = db_manager(self)
        self.db = self.db_manager.get_db_driver()

    def __repr__(self):
        return f"{self.name} v{self.version}"
    def _updatePlugins(self):
        pass
    def updatePlugins(self):
        self.logs_manager.updatePlugins()
        self._updatePlugins()

    def test(self):
        test_locale = LocaleClass(None,{'en': 'English', 'fr': 'French', 'ua': 'Ukrainian'}, 'en')
        second_locale = LocaleClass(1, {'en': 'Second_English', 'fr': 'Second_French', 'ua': 'Українська друга'}, 'en')

        self.db.add_locale(test_locale)
        self.db.add_locale(second_locale)
        self.logger.info(self, "test info")
        self.logger.debug(self, "test debug")
        self.logger.error(self, "test error")
        print(self.plugin_manager.getAllPluginsInfo())
        self.plugin_manager.enablePlugin("dummy_plugin")
        self.logger.info(self, "test info")
        test = self.plugin_manager.doCommand(self, 'Test', 'dummy_plugin', 'test_message')
        self.plugin_manager.disablePlugin("dummy_plugin")
        print(test)