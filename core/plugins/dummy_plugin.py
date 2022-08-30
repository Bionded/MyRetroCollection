
class dummy_plugin():
    def __init__(self, plugin_manager):
        self.name = "dummy_plugin"
        self.version = "0.0.1"
        self.author = "Bionded"
        self.plugin_type = "core"
        self.description = "This is a test plugin"
        self.website = ""
        self.license = "GPLv3"
        self.dependencies = []
        self.plugin_manager = plugin_manager
        self.logger = self.plugin_manager.logger

    def enable(self):
        self.logger.info(self, f"Plugin {self.name} enabled")

    def disable(self):
        self.logger.info(self, f"Plugin {self.name} disabled")

    def OnLoad(self):
        self.logger.info(self, f"Plugin {self.name} loaded")

    def OnUnload(self):
        self.logger.info(self, f"Plugin {self.name} unloaded")

    def OnTest(self, sender, test_string):
        self.logger.info(self, f"Runned from {sender} Plugin {self.name} test: {test_string}")
        return f"Runned from {sender} Test string: " + test_string