import os
import sys

class plugin_manager():
    '''
    init plugin manager
    '''
    def __init__(self, core):
        self.__core = core
        self.logger = self.__core.logger
        self.available_plugins = {}
        self.enabled_plugins = {}
        self.plugin_folder = "core/plugins"
        self.On_load_plugins_list = []
        self.On_unload_plugins_list = []
        self.getAvailablePlugins()


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
                    self.logger.error(f"Plugin {plugin_name} can't load, not found enable function, maybe you forgot to add it? Or maybe you have a wrong class name in main.py")
            if plugin.endswith(".py") and not plugin.startswith("_"):
                plugin_name = plugin.split(".")[0]
                plugin_module = __import__(f"{import_plugin_dir}.{plugin_name}")
                plugin_module =getattr(plugin_module,'plugins')
                while plugin_name in dir(plugin_module):
                    plugin_module = getattr(plugin_module, plugin_name,)
                if 'enable' in dir(plugin_module):
                    self.available_plugins[plugin_name] = plugin_module(self)
                else:
                    print(f"Plugin {plugin_name} can't load, something is wrong")

    def enableAllPlugins(self):
        for plugin in self.available_plugins.keys():
            self.enablePlugin(plugin)

    def enablePlugin(self, plugin_name):
        if plugin_name in self.available_plugins:
            self.enabled_plugins[plugin_name] = self.available_plugins[plugin_name]()
            for function in dir(self.enabled_plugins[plugin_name]):
                if function.startswith("On_"):
                    if function == "On_Load":
                        self.On_load_plugins_list.append(plugin_name)
                    elif function == "On_Unload":
                        self.On_unload_plugins_list.append(plugin_name)
                    else:
                        setattr(self, function, getattr(self.enabled_plugins[plugin_name], function))
            self.enabled_plugins[plugin_name].enable()
        else:
            print(f"Plugin {plugin_name} not found")

    def disablePlugin(self, plugin_name):
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins[plugin_name].disable()
            del self.enabled_plugins[plugin_name]
        else:
            print(f"Plugin {plugin_name} not found")

    def getPlugin(self, plugin_name):
        if plugin_name in self.enabled_plugins:
            return self.enabled_plugins[plugin_name]
        else:
            return None

    def OnLoad(self):
        for plugin in self.On_load_plugins_list:
            self.enabled_plugins[plugin].OnLoad()

    def getPluginInfo(self, plugin_name):
        if plugin_name in self.available_plugins.keys():
            if 'info' in dir(self.available_plugins[plugin_name]):
                return self.available_plugins[plugin_name].info()

            else:
                return f"{self.available_plugins[plugin_name].name} | {self.available_plugins[plugin_name].version} | " \
                   f"{self.available_plugins[plugin_name].description}"
        else:
            self.logger.error(f"Plugin {plugin_name} not found")

    def getAllPluginsInfo(self):
        info = []
        for plugin in self.available_plugins.keys():
            info.append(self.getPluginInfo(plugin))
        return info