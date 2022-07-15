import configparser
import os
import logging


class config_manager:
    def __init__(self, core):
        self.name = "config_manager"
        self.default_config_folder = 'config'
        self.default_config_file = 'retro_collection.conf'
        self.__core = core


    def getConfig(self, caller):
        return configs(caller, self)

class configs:
    def __init__(self, caller, config_manager):
        self.name = caller.name + '_config'
        self.__caller = caller
        self.__config_manager = config_manager
        self.logger = self.__caller.logger
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

    def getValue(self, key,_fallback=None):
        try:
            self.logger.debug(self, f"Getting value for {key} from {self.config_file_path}")
            return self.config.get(self.section, key, fallback=_fallback)
        except:
            self.logger.debug(self, f"Error getting value for {key} from {self.config_file_path}")
            return _fallback

    def setValue(self, key, value):
        try:
            self.logger.debug(self, f"Setting value for {key} to {value} in {self.config_file_path}")
            self.config.set(self.section, key, value)
        except:
            self.logger.debug(self, f"Error setting value for {key} to {value} in {self.config_file_path}")
            return False
        return True

    def getBool(self, key, _fallback=None):
        try:
            self.logger.debug(self, f"Getting bool for {key} from {self.config_file_path}")
            return self.config.getboolean(self.section, key, fallback=_fallback)
        except:
            self.logger.debug(self, f"Error getting bool for {key} from {self.config_file_path}")
            return _fallback

    def getInt(self, key, _fallback=None):
        try:
            self.logger.debug(self, f"Getting int for {key} from {self.config_file_path}")
            return self.config.getint(self.section, key, fallback=_fallback)
        except:
            self.logger.debug(self, f"Error getting int for {key} from {self.config_file_path}")
            return _fallback

    def getFloat(self, key, _fallback=None):
        try:
            self.logger.debug(self, f"Getting float for {key} from {self.config_file_path}")
            return self.config.getfloat(self.section, key, fallback=_fallback)
        except:
            self.logger.debug(self, f"Error getting float for {key} from {self.config_file_path}")
            return _fallback


    def getAllValues(self):
        try:
            self.logger.debug(self, f"Getting all values from {self.config_file_path}")
            return self.config.items(self.section)
        except:
            self.logger.debug(self, f"Error getting all values from {self.config_file_path}")
            return False

    def getAllSections(self):
        try:
            self.logger.debug(self, f"Getting all sections from {self.config_file_path}")
            return self.config.sections()
        except:
            self.logger.error(self, f"Error getting all sections from {self.config_file_path}")
            return False

    def saveConfig(self):
        try:
            self.logger.debug(self, f"Saving {self.config_file_path}")
            with open(self.config_file_path, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            self.logger.error(self, f"Error saving {self.config_file_path}")
            self.logger.error(e)
            return False
        return True

    def reloadConfig(self):
        try:
            self.logger.debug(self, f"Loading {self.config_file_path}")
            self.config.read(self.config_file_path)
        except:
            self.logger.error(self, f"Error loading {self.config_file_path}")
            return False
        return True
