import configparser
import logging


class Config_manager:
    def __init__(self, _config_path='config/base.conf', _logger=logging.getLogger("__main__")):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config_file = _config_path
        self.config.read(self.config_file)
        self.section = None
        self.logger = _logger
        self.logger.debug(msg=f"Config {self.section} initiated!")
        if self.section not in self.config.sections():
            self.logger.info(msg=f"In config file '{self.config_file}', Section '{self.section}' not exist!")



    def set_section(self, section: str):
        self.section = section
        return self

    def get(self, _param='def', _fallback=None):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            value = self.config.get(self.section, _param, fallback=_fallback)
            self.logger.info(f"Value: {value} from param {_param} in section {self.section}")
            return value
        except Exception as e:
            self.logger.critical(f"Get value error: {e}", exc_info=True)
            return _fallback

    def get_bool(self, _param='def', _fallback=None):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            value = self.config.getboolean(self.section, _param, fallback=_fallback)
            self.logger.info(f"Value: {value} from param {_param} in section {self.section}")
            return value
        except Exception as e:
            self.logger.critical(f"Get value error: {e}", exc_info=True)
            return _fallback

    def get_int(self, _param='def', _fallback=None):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            value = self.config.getint(self.section, _param, fallback=_fallback)
            self.logger.info(f"Value: {value} from param {_param} in section {self.section}")
            return value
        except Exception as e:
            self.logger.critical(f"Get value error: {e}", exc_info=True)
            return _fallback

    def set(self, _param='def', _value=None):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, _value)
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def set_bool(self, _param='def', _value=True):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, str(_value))
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def set_int(self, _param='def', _value=0):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, str(_value))
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def save(self):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            with open(self.config_file, 'rw') as configfile:  # save
                self.config.write(configfile)
            self.logger.info(f"Config save to file '{self.config_file}'Success!")
        except Exception as e:
            self.logger.critical(f"Saving config error: {e}", exc_info=True)

    def reload(self):
        if not self.section:
            self.logger.info(f"Section not configured. Please use .Section()")
            return None
        try:
            self.config.read(self.config_file)
            self.logger.info(f"Config reload from file '{self.config_file}'Success!")
        except Exception as e:
            self.logger.critical(f"Reload config error: {e}", exc_info=True)
