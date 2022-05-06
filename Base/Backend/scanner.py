import time
import json
from Base.Backend.Classes import platform, importer, romdb
import logging
from Base import configger
import os
from queue import Queue
import threading
import atexit

supported_platforms = [
    'gba',
    'nes',
    'snes',
    'psx',
    'psp',
    'gb',
    'gbc',
    'megadrive',
    'dreamcast',
]

class Rom_scanner:
    def __init__(self, _conf_path="config/base.conf", _logger=logging.getLogger("__main__")):
        self.logger = _logger
        self.scan_config = configger.Configger(_conf_path, "Scanner")
        self.base_rom_folder = self.scan_config.get("base_folder", "ROMS")
        self.platforms_templates = self.load_templates()
        self.max_threads = self.scan_config.get_int("max_threads", 1)
        self.supported_platforms = self.scan_config.get("supported_platforms", []).strip('][').split(', ')
        self.platforms = self.load_platoforms()
        self.importers = importer.Importer()
        atexit.register(self.close_platform)


        self.files_dict = {}
        self.queue = Queue()
        self.start_threads()


    def start_threads(self):
        for x in range(self.max_threads):
            thread = threading.Thread(target=self.daemon)
            thread.daemon = True
            thread.start()

    def daemon(self):
        while True:
            time.sleep(1)
            job = self.queue.get()
            thread = threading.Thread(target=job['func'], args=job['args'])
            thread.start()
            thread.join()
            self.queue.task_done()

###########################################

    def load_platoforms(self):
        platforms = {}
        for tplatform in self.supported_platforms:
            filepath = os.path.join(self.base_rom_folder, tplatform, 'platform.json')
            platforms[tplatform] = romdb.getDB(filepath)
            if platforms[tplatform].get_platform() == platform.Platform():
                new_platform = self.get_platform_template(tplatform)
                platforms[tplatform].set_platform(new_platform)


        return platforms

    def get_platform_template(self, name:str):
        if name in self.platforms_templates.keys():
            return platform.Platform().fromDict(self.platforms_templates[name])

    def load_templates(self):
        with open(self.scan_config.get("platform_templates", "DB/templates/platforms.json")) as json_file:
            return json.load(json_file)

    def close_platform(self):
        for platform in self.platforms.values():
            platform.close()

    def import_collection(self, _filepath, platform_name):
        self.queue.put({'func': self.__import_collection, 'args': (_filepath, platform_name,)})

    def __import_collection(self, _filepath, platform_name):
        try:
            if platform_name in self.supported_platforms:
                roms = self.importers.import_file(_filepath)
                self.platforms[platform_name].addMany(roms)
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Error: {e}")

    def __scan_folder(self,folder):
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]

    def __scan_platform(self, platform_name: str):
        with self.platforms[platform_name].get_platform() as pltfrm:
            path_to_platform = os.path.join(self.base_rom_folder, pltfrm.folder)



















    # def start_scan(self, _folder='/Volumes/Bionded/Roms/gba'):
    #     self.queue.put({'func': self.__scan_folder, 'args': (_folder,), 'name': f'Scan {_folder}'})
    #
    # def __scan_folder(self, _folder):
    #     for f in listdir(_folder):
    #         if path.isfile(path.join(_folder, f)):
    #             self.files_dict[f] = self.md5(path.join(_folder, f))
    #
    #     return "IAM FINISH!"



    def send(self, _message):
        self.logger.info(f"Message: {_message}")
        return f"Message: {_message}"
