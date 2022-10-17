import os
import sys

class plugin_manager():
    '''
    init plugin manager
    '''
    def __init__(self, core):
        self.name = "plugin_manager"
        self.config_section = "PluginManager"
        self.version = "0.0.1"
        self._core = core
        self.config_manager = self._core.config_manager
        self.config = self.config_manager.getConfig(self)
        self.logs_manager = self._core.logs_manager
        self.logger = self.logs_manager.getLogger(called_by=self)
        self.available_plugins = {}
        self.enabled_plugins = {}
        self.plugin_folder = os.path.join(os.path.basename(self._core.folder), "plugins")
        self.allowed_plugin_types =self.config.getValue('allowedPluginTypes', 'logger,db_driver,fs_driver,dummy,core,api,exporter,importer,scraper').split(',')
        self.functions = {}
        self.getAvailablePlugins()

    def __repr__(self):
        return f"{self.name} v{self.version}"

    def enable(self):
        for plugin_name in self.config.getValue('enabledPlugins', '').split(','):
            plugin_name = plugin_name.strip()
            if plugin_name != '':
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
                if 'enable' in dir(plugin_module) and 'disable' in dir(plugin_module):
                    if plugin_module.type in self.allowed_plugin_types:
                        self.available_plugins[plugin_name] = plugin_module(self)
                    else:
                        self.logger.error(self, f"Plugin {plugin_name} can't load, plugin type {plugin_module.type} not allowed")
                else:
                    self.logger.error(self, f"Plugin {plugin_name} can't load, not found enable or disable function, maybe you forgot to add it? Or maybe you have a wrong class name in main.py")
            if plugin.endswith(".py") and not plugin.startswith("_"):
                plugin_name = plugin.split(".")[0]
                plugin_module = __import__(f"{import_plugin_dir}.{plugin_name}")
                plugin_module =getattr(plugin_module,'plugins')
                while plugin_name in dir(plugin_module):
                    plugin_module = getattr(plugin_module, plugin_name,)
                if 'enable' in dir(plugin_module) and 'disable' in dir(plugin_module):
                    if plugin_module.type in self.allowed_plugin_types:
                        self.available_plugins[plugin_name] = plugin_module(self)
                    else:
                        self.logger.error(self, f"Plugin {plugin_name} can't load, plugin type {plugin_module.type} not allowed")
                else:
                    self.logger.error(self, f"Plugin {plugin_name} can't load, not found enable or disable function, maybe you forgot to add it? Or maybe you have a wrong class name")

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
            self._core.updatePlugins()
            self.logger.info(self, f"Plugin {plugin_name} enabled")
        elif plugin_name in self.enabled_plugins:
            self.logger.info(self, f"Plugin {plugin_name} already enabled")
        else:
            self.logger.error(self, f"Plugin {plugin_name} not found")
            self.disablePlugin(plugin_name)

    def disablePlugin(self, plugin_name):
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins[plugin_name].disable()
            del self.enabled_plugins[plugin_name]
            self._core.updatePlugins()
            if plugin_name in self.config.getValue('enabledPlugins', '').split(','):
                enabled_plugins = self.config.getValue('enabledPlugins', '').split(',')
                enabled_plugins.remove(plugin_name)
                self.config.setValue('enabledPlugins', ','.join(enabled_plugins))
                self.config.saveConfig()
                self._core.updatePlugins()
                self.logger.info(self, f"Plugin {plugin_name} disabled")
        elif plugin_name in self.config.getValue('enabledPlugins', '').split(','):
                enabled_plugins = self.config.getValue('enabledPlugins', '').split(',')
                enabled_plugins.remove(plugin_name)
                self.config.setValue('enabledPlugins', ','.join(enabled_plugins))
                self.config.saveConfig()
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
                   f"{self.available_plugins[plugin_name].description} | {self.available_plugins[plugin_name].author}"
        else:
            self.logger.error(self, f"Plugin {plugin_name} not found")

    def getAllPluginsInfo(self):
        info = []
        for plugin in self.available_plugins.keys():
            info.append(self.getPluginInfo(plugin))
        return info

    def doCommand(self, sender, command, plugin_name=None, *args, **kwargs):
        do_command = 'On' + command
        if plugin_name is None:
            if do_command in self.functions.keys():
                for plugin in self.functions[do_command]:
                    return getattr(self.enabled_plugins[plugin], do_command)(sender, *args, **kwargs)
            else:
                return None
        else:
            if do_command in self.functions.keys():
                if plugin_name in self.functions[do_command]:
                    return getattr(self.enabled_plugins[plugin_name], do_command)(sender, *args, **kwargs)
                else:
                    return None
            else:
                return None
