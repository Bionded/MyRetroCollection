from core.utils.types import PluginBody


class dummy_plugin(PluginBody):
    name = "dummy_plugin"   # Plugin name must be the same as file name and class name
    version = "0.0.1"
    author = "Bionded"
    plugin_type = "dummy"
    type = plugin_type
    description = "This is a test plugin"
    website = ""
    different_log = True
    log_file = "dummy.log"
    license = "GPLv3"
    dependencies = []

    #Enable and disable function is required
    def enable(self):
        self.logger.info(self, f"Plugin {self.name} enabled")

    def disable(self):
        self.logger.info(self, f"Plugin {self.name} disabled")

    def OnLoad(self):
        self.logger.info(self, f"Plugin {self.name} loaded")

    def OnUnload(self):
        self.logger.info(self, f"Plugin {self.name} unloaded")

    def OnTest(self, sender, test_string):
        self.logger.info(self, f"Runned from '{sender}' Plugin {self.name} test: {test_string}")
        return f"Runned from {sender} Test string: " + test_string

    def OnInfoLogger(self, sender, test_string):
        self.logger.info(self, f"Runned from '{sender}' Plugin {self.name} test: {test_string}")
        return f"Runned from {sender} Test string: " + test_string