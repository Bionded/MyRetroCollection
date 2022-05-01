import time
from Base.Backend.Classes import rom, collection, importer
from tinydb import TinyDB, Query
import logging
from Base import configger
from os import listdir, makedirs
from os.path import isfile, join, isdir, exists, splitext
import hashlib
from queue import Queue
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class Rom_scanner:
    def __init__(self, _conf_path="config/base.conf", _logger=logging.getLogger("__main__")):
        self.logger = _logger
        self.scan_config = configger.Configger(_conf_path, "Scanner")
        self.base_rom_folder = self.scan_config.get("base_folder", "ROMS")
        self.platform_dbs_dir = self.scan_config.get("platforms_db", "DB/platforms")
        self.max_threads = self.scan_config.get_int("max_threads", 1)
        self.platform_dbs = self.load_collections()
        self.importers = importer.Importer()


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
            time.sleep(2)
            job = self.queue.get()
            thread = threading.Thread(target=job['func'], args=job['args'])
            thread.start()
            thread.join()
            self.queue.task_done()

    def load_collections(self):
        platforms = {}
        configs = []
        if not exists(self.platform_dbs_dir):
            makedirs(self.platform_dbs_dir)
        elif isdir(self.platform_dbs_dir):
            configs = [f for f in listdir(self.platform_dbs_dir) if isfile(join(self.platform_dbs_dir, f))]
        else:
            self.logger.error(f"{self.platform_dbs_dir} may be folder! Not file")

        if configs != []:
            for conf in configs:
                name = splitext(conf)[0]
                try:
                    platforms[name] = TinyDB(join(self.platform_dbs_dir, conf))
                    self.logger.info(f"Platform {name} loaded!")
                except Exception as e:
                    self.logger.error(f"Error when {name} loading!")
                    self.logger.error(f"{e}")
        else:
            self.logger.info("No db files for platforms")
        return platforms

    def add_platform(self, _collection : collection.Collection):
        if not exists(self.platform_dbs_dir):
            makedirs(self.platform_dbs_dir)
        self.platform_dbs[_collection.name] = TinyDB(join(self.platform_dbs_dir, _collection.name + '.json'))


    def import_collection(self,_filepath):
        test = self.importers.import_file(_filepath)
        print(test)
        return test

    #def edit_platform(self):
















    def start_scan(self, _folder='/Volumes/Bionded/Roms/gba'):
        self.queue.put({'func': self.__scan_folder, 'args': (_folder,), 'name': f'Scan {_folder}'})

    def __scan_folder(self, _folder):
        for f in listdir(_folder):
            if isfile(join(_folder, f)):
                self.files_dict[f] = self.md5(join(_folder, f))

        return "IAM FINISH!"



    def send(self, _message):
        self.logger.info(f"Message: {_message}")
        return f"Message: {_message}"
