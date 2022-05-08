from Base.Backend import scanner, storage,collector,importer,scraper,filesystem
from Base import config_manager
from Base.logger import load_logger
import logging



class Backend:

    def __init__(self):
        conf_path = "config/backend.conf"
        self.configs = config_manager.Config_manager(conf_path)
        self.logger = load_logger(self.configs, "__Backend__")
        self.Filesystem = filesystem.getFS(config=self.configs, logger=self.logger)
        self.Storage = storage.SQLStorage(config=self.configs, logger=self.logger)
        self.Importer = importer.Importer(config=self.configs, logger=self.logger,
                                          fs=self.Filesystem)
        self.Scanner = scanner.FileScanner(config=self.configs, filesystem=self.Filesystem,
                                           logger=self.logger)
        self.Collector = collector.Collector(config=self.configs,storage=self.Storage,
                                             importer=self.Importer,filesystem=self.Filesystem, logger=self.logger)
    def test(self):
        self.Collector.test_scan('gba')

backend = Backend()
backend.test()