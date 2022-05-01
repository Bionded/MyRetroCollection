import configparser
import logging


class Configger:
    def __init__(self, _config_path='config/base.conf', _section="base", _logger=logging.getLogger("__main__")):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config_file = _config_path
        self.config.read(self.config_file)
        self.section = _section
        self.logger = _logger
        self.logger.debug(msg=f"Config {self.section} initiated!")
        if self.section not in self.config.sections():
            self.logger.info(msg=f"In config file '{self.config_file}', Section '{self.section}' not exist! Creating.")
            self.config.add_section(self.section)

    def get(self, _param='def', _fallback=None):
        try:
            value = self.config.get(self.section, _param, fallback=_fallback)
            self.logger.info(f"Value: {value} from param {_param} in section {self.section}")
            return value
        except Exception as e:
            self.logger.critical(f"Get value error: {e}", exc_info=True)
            return _fallback

    def get_bool(self, _param='def', _fallback=None):
        try:
            value = self.config.getboolean(self.section, _param, fallback=_fallback)
            self.logger.info(f"Value: {value} from param {_param} in section {self.section}")
            return value
        except Exception as e:
            self.logger.critical(f"Get value error: {e}", exc_info=True)
            return _fallback

    def get_int(self, _param='def', _fallback=None):
        try:
            value = self.config.getint(self.section, _param, fallback=_fallback)
            self.logger.info(f"Value: {value} from param {_param} in section {self.section}")
            return value
        except Exception as e:
            self.logger.critical(f"Get value error: {e}", exc_info=True)
            return _fallback

    def set(self, _param='def', _value=None):
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, _value)
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def set_bool(self, _param='def', _value=True):
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, str(_value))
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def set_int(self, _param='def', _value=0):
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, str(_value))
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def save(self):
        try:
            with open(self.config_file, 'rw') as configfile:  # save
                self.config.write(configfile)
            self.logger.info(f"Config save to file '{self.config_file}'Success!")
        except Exception as e:
            self.logger.critical(f"Saving config error: {e}", exc_info=True)

    def reload(self):
        try:
            self.config.read(self.config_file)
            self.logger.info(f"Config reload from file '{self.config_file}'Success!")
        except Exception as e:
            self.logger.critical(f"Reload config error: {e}", exc_info=True)
