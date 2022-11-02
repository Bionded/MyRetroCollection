class PluginBody:
    name = None
    version = None
    author = None
    type = None
    plugin_type = None
    description = None
    website = None
    license = None
    dependencies = []
    different_log = False
    log_file = None

    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.config = self.plugin_manager.config_manager.getConfig(self)
        self.logger = self.plugin_manager.logs_manager.getLogger(called_by=self)

    def __repr__(self):
        return f"{self.name} v{self.version}"

    def enable(self):
        pass

    def disable(self):
        pass

    def represent(self):
        return f"{self.name} v{self.version}"
