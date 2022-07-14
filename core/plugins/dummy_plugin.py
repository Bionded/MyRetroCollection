
class dummy_plugin():
    def __init__(self, plugin_manager):
        self.name = "dummy_plugin"
        self.version = "0.0.1"
        self.author = "Bionded"
        self.description = "This is a test plugin"
        self.website = ""
        self.license = "GPLv3"
        self.dependencies = []
        self.plugin_manager = plugin_manager
        pass

    def enable(self):
        print(f"Plugin {self.name} enabled")

    def disable(self):
        print(f"Plugin {self.name} disabled")

    def OnLoad(self):
        print(f"Plugin {self.name} loaded")

    def OnUnload(self):
        print(f"Plugin {self.name} unloaded")