import logging
from _Old.Base.config_manager import Config_manager
from queue import Queue
from _Old.Base.Backend.filesystem import getFS

class FileScanner:
    def __init__(self, filesystem=getFS(), config=Config_manager(), logger=logging.getLogger("__main__")):
        self.config = config.set_section("Scanner")
        self.logger = logger
        self.fs = filesystem
        self.queue =Queue()
        self.base_folder = self.config.get_bool("base_folder", '/Volumes/Bionded/Roms')

    def scan_platform(self, platform: dict):
        return self.fs.get_all_files(platform['folder'], platform['extensions'])



    def send(self, _message):
        self.logger.info(f"Message: {_message}")
        return f"Message: {_message}"
