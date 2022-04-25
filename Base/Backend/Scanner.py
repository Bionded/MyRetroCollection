from multiprocessing import pool, Process
from Classes import Rom,Platform
from Base import Configger


class Rom_scanner:
    def __init__(self, _conf_path="config/base.conf", ):
        self.scan_config = Configger.configger(_conf_path, "SCANNER")
        self.roms_config = Configger.configger(_conf_path, "ROMS")
        self.base_rom_folder = self.roms_config.get("base_folder", "ROMS")