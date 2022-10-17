import configparser
import os
import logging


class config_manager:
    def __init__(self, core):
        self.name = "config_manager"
        self.version = "0.0.1"
        self.default_config_folder = 'config'
        self.default_config_file = 'retro_collection.conf'
        self.__core = core

    def __repr__(self):
        return f"{self.name} v{self.version}"

    def getConfig(self, caller):
        return configs(caller, self)


class configs:
    def __init__(self, caller, config_manager):
        self.name = caller.name + '_config'
        self.__config_manager = config_manager
        self.version = self.__config_manager.version
        self.__caller = caller
        self.config = configparser.ConfigParser()
        try:
            self.config_file = caller.config_file
        except:
            self.config_file = self.__config_manager.default_config_file
        try:
            self.section = caller.config_section
        except:
            try:
                self.section = caller.name
            except:
                self.section = 'default'

        self.config_file_path = os.path.join(self.__config_manager.default_config_folder, self.config_file)
        self.reloadConfig()

    def __repr__(self):
        return f"{self.name} v{self.version}"

    def getValue(self, key, _fallback=None):
        try:
            return self.config.get(self.section, key, fallback=_fallback)
        except:
            return _fallback

    def setValue(self, key, value):
        try:
            self.config.set(self.section, key, value)
        except:
            return False
        return True

    def getBool(self, key, _fallback=None):
        try:
            return self.config.getboolean(self.section, key, fallback=_fallback)
        except:
            return _fallback

    def getInt(self, key, _fallback=None):
        try:
            return self.config.getint(self.section, key, fallback=_fallback)
        except:
            return _fallback

    def getFloat(self, key, _fallback=None):
        try:
            return self.config.getfloat(self.section, key, fallback=_fallback)
        except:
            return _fallback


    def getAllValues(self):
        try:
            return self.config.items(self.section)
        except:
            return False

    def getAllSections(self):
        try:
            return self.config.sections()
        except:
            return False

    def saveConfig(self):
        try:
            with open(self.config_file_path, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f'Error saving config: {e}')
            return False
        return True

    def reloadConfig(self):
        try:
            self.config.read(self.config_file_path)
        except Exception as e:
            print(f'Error reading config file: {self.config_file_path} {e}')
            return False
        return True
