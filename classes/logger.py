import logging
import os
from classes import configger

def load_logger(_confpath="config/base.conf",_name="base"):
    conf = configger.Configger(_config_path=_confpath, _section="Logs")
    log_file = conf.get("log_file", "Logs/log.log")
    log_dir = os.path.dirname(log_file)
    formatting = conf.get("format", '%(asctime)s %(levelname)-8s %(message)s')
    date_format = conf.get("date_format", '%a, %d %b %Y %H:%M:%S')
    level = conf.get("level", "INFO")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_format = logging.Formatter(fmt=formatting,datefmt=date_format)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_format)
    logger = logging.getLogger(_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
