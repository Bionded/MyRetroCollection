import os
import sys

class plugin_manager():
    '''
    init plugin manager
    '''
    def __init__(self, core):
        self.name = "plugin_manager"
        self.config_section = "PluginManager"
        self.__core = core
        self.logger = self.__core.logs_manager.getLogger()
        self.config_manager = self.__core.config_manager
        self.config = self.config_manager.getConfig(self)
        self.available_plugins = {}
        self.enabled_plugins = {}
        self.plugin_folder = "core/plugins"
        self.functions = {}
        self.getAvailablePlugins()


    def enable(self):
        for plugin_name in self.config.getValue('enabledPlugins','').split(','):
            self.enablePlugin(plugin_name)

    def getAvailablePlugins(self):
        import_plugin_dir = self.plugin_folder.replace(os.sep, '.')
        sys.path.insert(0, self.plugin_folder)
        for plugin in os.listdir(self.plugin_folder):
            if os.path.isdir(f"{self.plugin_folder}/{plugin}") and 'main.py' in os.listdir(f"{self.plugin_folder}/{plugin}"):
                plugin_name = plugin
                plugin_module = __import__(f"{import_plugin_dir}.{plugin_name}.main")
                plugin_module =getattr(plugin_module,'plugins')
                while plugin_name in dir(plugin_module):
                    plugin_module = getattr(plugin_module, plugin_name)
                if 'enable' in dir(plugin_module):
                    self.available_plugins[plugin_name] = plugin_module(self)
                else:
                    self.logger.error(self, f"Plugin {plugin_name} can't load, not found enable function, maybe you forgot to add it? Or maybe you have a wrong class name in main.py")
            if plugin.endswith(".py") and not plugin.startswith("_"):
                plugin_name = plugin.split(".")[0]
                plugin_module = __import__(f"{import_plugin_dir}.{plugin_name}")
                plugin_module =getattr(plugin_module,'plugins')
                while plugin_name in dir(plugin_module):
                    plugin_module = getattr(plugin_module, plugin_name,)
                if 'enable' in dir(plugin_module):
                    self.available_plugins[plugin_name] = plugin_module(self)
                else:
                    self.logger.error(self, f"Plugin {plugin_name} can't load, not found enable function, maybe you forgot to add it? Or maybe you have a wrong class name")

    def enableAllPlugins(self):
        for plugin in self.available_plugins.keys():
            self.enablePlugin(plugin)

    def enablePlugin(self, plugin_name):
        if plugin_name in self.available_plugins and plugin_name not in self.enabled_plugins:
            self.enabled_plugins[plugin_name] = self.available_plugins[plugin_name]
            for function in dir(self.enabled_plugins[plugin_name]):
                if function.startswith("On") or function.startswith("Pre") or function.startswith("Post"):
                    if function not in self.functions.keys():
                        self.functions[function] = []
                        self.functions[function].append(plugin_name)
                    else:
                        self.functions[function].append(plugin_name)
            if plugin_name not in self.config.getValue('enabledPlugins', '').split(','):
                if self.config.getValue('enabledPlugins', '') == '':
                    self.config.setValue('enabledPlugins', plugin_name)
                else:
                    self.config.setValue('enabledPlugins', f"{self.config.getValue('enabledPlugins')},{plugin_name}")
                self.config.saveConfig()
            self.enabled_plugins[plugin_name].enable()
            self.logger.info(self, f"Plugin {plugin_name} enabled")
        elif plugin_name in self.enabled_plugins:
            self.logger.info(self, f"Plugin {plugin_name} already enabled")
        else:
            self.logger.error(self, f"Plugin {plugin_name} not found")

    def disablePlugin(self, plugin_name):
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins[plugin_name].disable()
            del self.enabled_plugins[plugin_name]
            if plugin_name in self.config.get(self.section, 'enabledPlugins').split(','):
                self.config.setValue('enabledPlugins', self.config.get(self.section, 'enabledPlugins').replace(f",{plugin_name}", ""))
                self.config_manager.saveConfig(self)
                self.logger.info(self, f"Plugin {plugin_name} disabled")
        else:
            self.logger.error(self, f"Plugin {plugin_name} not found")

    def getPlugin(self, plugin_name):
        if plugin_name in self.enabled_plugins:
            return self.enabled_plugins[plugin_name]
        else:
            return None

    def getPluginInfo(self, plugin_name):
        if plugin_name in self.available_plugins.keys():
            if 'info' in dir(self.available_plugins[plugin_name]):
                return self.available_plugins[plugin_name].info()

            else:
                return f"{self.available_plugins[plugin_name].name} | {self.available_plugins[plugin_name].version} | " \
                   f"{self.available_plugins[plugin_name].description}"
        else:
            self.logger.error(self, f"Plugin {plugin_name} not found")

    def getAllPluginsInfo(self):
        info = []
        for plugin in self.available_plugins.keys():
            info.append(self.getPluginInfo(plugin))
        return info

    def DoCommand(self, sender, command, *args,**kwargs):
        if command in self.functions.keys():
            for plugin in self.functions[command]:
                return getattr(self.enabled_plugins[plugin], command)(sender, *args, **kwargs)
        else:
            return None
