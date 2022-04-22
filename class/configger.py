import configparser

import base_class.Logger
class configger():
    def __init__(self,_config_path='config/base.ini', _section="base", _logger=None):
        self.config = configparser.ConfigParser()
        self.config_file = _config_path
        self.config.read(self.config_file)
        self.section = _section
        self.logger = _logger
        self.logger.debug(f"Config {self.section} initiated!")
        if self.section not in self.config.sections():
            self.logger.info(f"In config file '{self.config_file}', Section '{self.section}' not exist! Creating.")
            self.config.add_section(self.section)

    def get(self, _param='def',_fallback=None):
        Value = self.config.get(self.section, _param, fallback=_fallback)
        self.logger.debug(f"Value: {Value} from param {_param} in section {self.section}")
        return

    def set(self, _param='def', _value=None):
        try:
            self.logger.debug(f"Set Value: {_value} on param {_param} in section {self.section}")
            self.config.set(self.section, _param, _value)
            self.save()
            return True
        except Exception as e:
            self.logger.critical(f"Set value error: {e}", exc_info=True)
            return False

    def save(self):
        try:
            self.config.write()
            self.logger.info(f"Config save to file '{self.config_file}'Success!")
        except Exception as e:
            self.logger.critical(f"Saving config error: {e}", exc_info=True)

    def reload(self):
        try:
            self.config.read(self.config_file)
            self.logger.info(f"Config reload from file '{self.config_file}'Success!")
        except Exception as e:
            self.logger.critical(f"Reload config error: {e}", exc_info=True)
